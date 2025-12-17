"""
Codebase analyzer tool for detecting languages and frameworks.
"""
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set

from crewai_tools import BaseTool
from pydantic import Field as PydanticField


@dataclass
class AnalysisConfig:
    """Configuration for codebase analysis."""
    
    language_extensions: Dict[str, List[str]] = field(default_factory=lambda: {
        "JavaScript": [".js", ".jsx", ".mjs"],
        "TypeScript": [".ts", ".tsx"],
        "Ruby": [".rb"],
        "HTML": [".html", ".htm"],
        "CSS": [".css", ".scss", ".sass"],
        "Apex": [".cls", ".trigger"],
        "Python": [".py"],
        "Java": [".java"],
        "C#": [".cs"],
    })
    
    framework_indicators: Dict[str, List[str]] = field(default_factory=lambda: {
        "React": ["package.json", "src/App.jsx", "src/App.js"],
        "Ruby on Rails": ["Gemfile", "config/application.rb", "app/controllers/"],
        "Salesforce": ["sfdx-project.json", "force-app/", ".sfdx/"],
        "Vue": ["vue.config.js", "src/main.js"],
        "Angular": ["angular.json", "src/app/"],
    })
    
    key_files: Set[str] = field(default_factory=lambda: {
        "package.json", "Gemfile", "requirements.txt", "pom.xml", "csproj"
    })
    
    excluded_dirs: Set[str] = field(default_factory=lambda: {
        "node_modules", "__pycache__", "target", "build", "dist", ".git", "vendor"
    })


class CodebaseAnalyzer:
    """Analyzes a codebase to detect technologies and structure."""
    
    def __init__(self, config: AnalysisConfig = None):
        self._config = config or AnalysisConfig()
    
    def analyze(self, directory: str) -> Dict:
        """Analyze directory and return detected technologies."""
        result = {
            "languages": [],
            "frameworks": [],
            "key_files": [],
        }
        
        languages: Set[str] = set()
        frameworks: Set[str] = set()
        key_files: List[str] = []
        
        for root, dirs, files in os.walk(directory):
            self._filter_directories(dirs)
            
            for filename in files:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, directory)
                
                self._detect_language(filename, languages)
                self._detect_framework(rel_path, filename, frameworks)
                self._collect_key_file(filename, rel_path, key_files)
        
        result["languages"] = sorted(languages)
        result["frameworks"] = sorted(frameworks)
        result["key_files"] = key_files
        
        return result
    
    def _filter_directories(self, dirs: List[str]) -> None:
        """Remove excluded directories from traversal."""
        dirs[:] = [
            d for d in dirs 
            if not d.startswith(".") and d not in self._config.excluded_dirs
        ]
    
    def _detect_language(self, filename: str, languages: Set[str]) -> None:
        """Detect programming language from file extension."""
        ext = Path(filename).suffix.lower()
        for language, extensions in self._config.language_extensions.items():
            if ext in extensions:
                languages.add(language)
                break
    
    def _detect_framework(
        self, 
        rel_path: str, 
        filename: str, 
        frameworks: Set[str]
    ) -> None:
        """Detect framework from file indicators."""
        for framework, indicators in self._config.framework_indicators.items():
            for indicator in indicators:
                if indicator in rel_path or filename == indicator:
                    frameworks.add(framework)
                    break
    
    def _collect_key_file(
        self, 
        filename: str, 
        rel_path: str, 
        key_files: List[str]
    ) -> None:
        """Collect important project files."""
        if filename in self._config.key_files:
            key_files.append(rel_path)


class FileAnalyzerTool(BaseTool):
    """CrewAI tool wrapper for codebase analysis."""
    
    name: str = "File Analyzer"
    description: str = "Analyzes a codebase to detect languages, frameworks, and structure"
    base_path: str = PydanticField(default=".")
    
    def _run(self, directory: str = None) -> str:
        """Execute analysis and return JSON result."""
        target = directory or self.base_path
        analyzer = CodebaseAnalyzer()
        result = analyzer.analyze(target)
        return json.dumps(result, indent=2)
