"""
Orchestrator for backlog card processing.
Coordinates analysis and delegates to specialized framework crews.
"""
import json
import logging
import re
from typing import Dict, List

from crewai import Agent, Crew, Task
from langchain_openai import ChatOpenAI
from textwrap import dedent

from .entities import AnalysisResult, BacklogCard
from .config import Settings
from .slack import create_slack_service, HumanInteractionService

logger = logging.getLogger(__name__)


class ToolsProvider:
    """Provides tools for agents - Dependency Injection pattern."""
    
    def __init__(self, enable_human_input: bool = False):
        from crewai_tools import FileReadTool
        from langchain_community.tools import DuckDuckGoSearchRun
        from tools.analyzer import FileAnalyzerTool
        from tools.filesystem import FileWriteTool, DirWriteTool
        from tools.human_input import HumanInputTool
        
        self.search = DuckDuckGoSearchRun()
        self.file_read = FileReadTool()
        self.file_write = FileWriteTool.file_write_tool
        self.dir_write = DirWriteTool.dir_write_tool
        self.analyzer = FileAnalyzerTool()
        self.ask_user = HumanInputTool.ask_user
        self.send_update = HumanInputTool.send_update
        self._enable_human_input = enable_human_input
    
    def get_architect_tools(self) -> List:
        """Get tools for architect - includes human input if enabled."""
        tools = [self.search, self.file_read, self.file_write, self.dir_write]
        if self._enable_human_input:
            tools.extend([self.ask_user, self.send_update])
        return tools
    
    def get_developer_tools(self) -> List:
        """Get tools for developers - includes status updates if enabled."""
        tools = [self.file_read, self.file_write, self.dir_write]
        if self._enable_human_input:
            tools.append(self.send_update)
        return tools


class CodebaseAnalyzer:
    """Analyzes existing codebase to detect technologies."""
    
    def __init__(self, tools: ToolsProvider):
        self._analyzer = tools.analyzer
    
    def analyze(self, project_path: str) -> Dict:
        """Analyze codebase and return technology information."""
        try:
            result = self._analyzer._run(project_path)
            return json.loads(result)
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Codebase analysis failed: {e}")
            return {"languages": [], "frameworks": [], "key_files": []}


class CardAnalyzer:
    """Analyzes backlog cards to determine implementation approach."""
    
    def __init__(self, settings: Settings, tools: ToolsProvider):
        self._settings = settings
        self._tools = tools
        self._llm = ChatOpenAI(
            model_name=settings.openai_model,
            temperature=settings.openai_temperature,
        )
    
    def analyze(self, card: BacklogCard, codebase_info: Dict) -> AnalysisResult:
        """Analyze card and codebase to determine implementation approach."""
        agent = self._create_orchestrator_agent()
        task = self._create_analysis_task(agent, card, codebase_info)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=self._settings.verbose_agents,
        )
        
        result = crew.kickoff()
        return self._parse_result(result, card.description)
    
    def _create_orchestrator_agent(self) -> Agent:
        return Agent(
            role="Technical Orchestrator",
            backstory=dedent("""\
                You are an experienced technical architect who analyzes requirements 
                and determines the best implementation approach. You understand multiple 
                frameworks and can identify the right tools for each task."""),
            goal=dedent("""\
                Analyze backlog cards and codebases to determine which framework 
                should handle implementation and extract technical requirements."""),
            tools=[self._tools.search, self._tools.file_read],
            allow_delegation=False,
            verbose=self._settings.verbose_agents,
            llm=self._llm,
        )
    
    def _create_analysis_task(
        self, 
        agent: Agent, 
        card: BacklogCard, 
        codebase_info: Dict
    ) -> Task:
        return Task(
            description=dedent(f"""\
                Analyze this backlog card and codebase to determine:
                
                BACKLOG CARD:
                {card.to_summary()}
                
                CODEBASE ANALYSIS:
                {json.dumps(codebase_info, indent=2)}
                
                Provide:
                1. Primary framework/language (React JS, Ruby on Rails, Apex, or HTML/CSS/JS)
                2. Files to modify
                3. Files to create
                4. Technical requirements
                5. Dependencies needed
                
                Output as JSON with keys: framework, files_to_modify, 
                files_to_create, requirements, dependencies."""),
            expected_output="JSON analysis with technical requirements",
            tools=[self._tools.search, self._tools.file_read],
            agent=agent,
        )
    
    def _parse_result(self, result: str, fallback_description: str) -> AnalysisResult:
        try:
            json_match = re.search(r"\{.*\}", str(result), re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return AnalysisResult(
                    framework=data.get("framework", "HTML/CSS/JS"),
                    files_to_modify=data.get("files_to_modify", []),
                    files_to_create=data.get("files_to_create", []),
                    requirements=data.get("requirements", ""),
                    dependencies=data.get("dependencies", []),
                )
        except (json.JSONDecodeError, AttributeError) as e:
            logger.warning(f"Failed to parse analysis result: {e}")
        
        return AnalysisResult.default(fallback_description)


class CrewFactory:
    """Factory for creating framework-specific crews."""
    
    def __init__(self, settings: Settings, tools: ToolsProvider):
        self._settings = settings
        self._tools = tools
    
    def create(self, framework: str, analysis: AnalysisResult) -> Crew:
        """Create appropriate crew based on detected framework."""
        framework_lower = framework.lower()
        
        if "react" in framework_lower:
            return self._create_react_crew(analysis)
        elif "rails" in framework_lower or "ruby" in framework_lower:
            return self._create_rails_crew(analysis)
        elif "apex" in framework_lower or "salesforce" in framework_lower:
            return self._create_apex_crew(analysis)
        else:
            return self._create_frontend_crew(analysis)
    
    def _create_react_crew(self, analysis: AnalysisResult) -> Crew:
        from frameworks.react.agents import ReactAgents
        from frameworks.react.tasks import ReactTasks
        return self._build_crew(ReactAgents(), ReactTasks(), analysis, "react")
    
    def _create_rails_crew(self, analysis: AnalysisResult) -> Crew:
        from frameworks.rails.agents import RailsAgents
        from frameworks.rails.tasks import RailsTasks
        return self._build_crew(RailsAgents(), RailsTasks(), analysis, "rails")
    
    def _create_apex_crew(self, analysis: AnalysisResult) -> Crew:
        from frameworks.apex.agents import ApexAgents
        from frameworks.apex.tasks import ApexTasks
        return self._build_crew(ApexAgents(), ApexTasks(), analysis, "apex")
    
    def _create_frontend_crew(self, analysis: AnalysisResult) -> Crew:
        from frameworks.frontend.agents import FrontendAgents
        from frameworks.frontend.tasks import FrontendTasks
        return self._build_crew(FrontendAgents(), FrontendTasks(), analysis, "frontend")
    
    def _build_crew(self, agents_factory, tasks_factory, analysis: AnalysisResult, prefix: str) -> Crew:
        architect_tools = self._tools.get_architect_tools()
        dev_tools = self._tools.get_developer_tools()
        
        architect = getattr(agents_factory, f"{prefix}_architect")(architect_tools)
        programmer = getattr(agents_factory, f"{prefix}_programmer")(dev_tools)
        tester = getattr(agents_factory, f"{prefix}_tester")(dev_tools)
        reviewer = getattr(agents_factory, f"{prefix}_reviewer")(dev_tools)
        
        analysis_dict = {
            "framework": analysis.framework,
            "files_to_modify": analysis.files_to_modify,
            "files_to_create": analysis.files_to_create,
            "requirements": analysis.requirements,
            "dependencies": analysis.dependencies,
        }
        
        arch_task = getattr(tasks_factory, f"{prefix}_architecture_task")(architect, analysis_dict)
        impl_task = getattr(tasks_factory, f"{prefix}_implementation_task")(programmer, [arch_task])
        test_task = getattr(tasks_factory, f"{prefix}_testing_task")(tester, [impl_task])
        review_task = getattr(tasks_factory, f"{prefix}_reviewing_task")(reviewer, [arch_task, impl_task, test_task])
        
        return Crew(
            agents=[architect, programmer, tester, reviewer],
            tasks=[arch_task, impl_task, test_task, review_task],
            verbose=self._settings.verbose_agents,
        )


class BacklogOrchestrator:
    """
    Main orchestrator for processing backlog cards.
    Coordinates analysis and execution of specialized crews.
    Supports human-in-the-loop via Slack integration.
    """
    
    def __init__(self, card: BacklogCard, project_path: str, settings: Settings):
        self._card = card
        self._project_path = project_path
        self._settings = settings
        self._slack_service = self._setup_slack_service()
        self._tools = ToolsProvider(enable_human_input=settings.is_slack_configured)
        self._codebase_analyzer = CodebaseAnalyzer(self._tools)
        self._card_analyzer = CardAnalyzer(settings, self._tools)
        self._crew_factory = CrewFactory(settings, self._tools)
    
    def _setup_slack_service(self) -> HumanInteractionService:
        """Initialize Slack service and configure human input tools."""
        from tools.human_input import set_interaction_service
        
        service = create_slack_service(
            token=self._settings.slack_token,
            channel=self._settings.slack_channel,
            use_console=not self._settings.is_slack_configured,
            poll_interval=self._settings.slack_poll_interval,
            timeout=self._settings.slack_timeout,
        )
        
        set_interaction_service(service)
        return service
    
    def execute(self) -> str:
        """Execute the complete backlog card processing pipeline."""
        logger.info("Starting backlog card analysis")
        
        # Start Slack session if configured
        if self._settings.is_slack_configured:
            self._slack_service.start_session(self._card.title)
        
        codebase_info = self._codebase_analyzer.analyze(self._project_path)
        analysis = self._card_analyzer.analyze(self._card, codebase_info)
        
        logger.info(f"Framework detected: {analysis.framework}")
        logger.info(f"Files to modify: {analysis.files_to_modify}")
        logger.info(f"Files to create: {analysis.files_to_create}")
        
        crew = self._crew_factory.create(analysis.framework, analysis)
        
        logger.info("Executing specialized crew")
        result = crew.kickoff()
        
        # Send completion to Slack
        if self._settings.is_slack_configured:
            self._slack_service.send_completion(
                f"Implementation completed for: {self._card.title}"
            )
        
        logger.info("Processing complete")
        return str(result)
