"""
Domain entities for the MultiAgent Developer application.
Following Clean Architecture - entities are at the core of the domain.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List


@dataclass
class BacklogCard:
    """
    Domain entity representing a normalized backlog card.
    Immutable representation of a task from any backlog system.
    """
    title: str
    description: str
    original_format: str
    acceptance_criteria: List[str] = field(default_factory=list)
    priority: Optional[str] = None
    story_points: Optional[int] = None
    labels: List[str] = field(default_factory=list)
    assignee: Optional[str] = None
    reporter: Optional[str] = None
    due_date: Optional[datetime] = None
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    attachments: List[str] = field(default_factory=list)

    def to_summary(self) -> str:
        """Generate a formatted summary of the card."""
        ac_text = "\n".join(f"- {ac}" for ac in self.acceptance_criteria) if self.acceptance_criteria else "None specified"
        
        return f"""TITLE: {self.title}
PRIORITY: {self.priority or 'Not set'}
STORY POINTS: {self.story_points or 'Not set'}
LABELS: {', '.join(self.labels) if self.labels else 'None'}
ASSIGNEE: {self.assignee or 'Not assigned'}

DESCRIPTION:
{self.description}

ACCEPTANCE CRITERIA:
{ac_text}"""

    def to_markdown(self) -> str:
        """Convert card to markdown format."""
        output = f"# {self.title}\n\n"
        output += f"## Description\n{self.description}\n\n"
        
        if self.acceptance_criteria:
            output += "## Acceptance Criteria\n"
            output += "\n".join(f"- {ac}" for ac in self.acceptance_criteria)
            output += "\n\n"
        
        metadata = []
        if self.priority:
            metadata.append(f"**Priority:** {self.priority}")
        if self.story_points:
            metadata.append(f"**Story Points:** {self.story_points}")
        if self.labels:
            metadata.append(f"**Labels:** {', '.join(self.labels)}")
        if self.assignee:
            metadata.append(f"**Assignee:** {self.assignee}")
        
        if metadata:
            output += "## Metadata\n" + "\n".join(metadata) + "\n"
        
        return output


@dataclass
class AnalysisResult:
    """Result of analyzing a backlog card against a codebase."""
    framework: str
    files_to_modify: List[str] = field(default_factory=list)
    files_to_create: List[str] = field(default_factory=list)
    requirements: str = ""
    dependencies: List[str] = field(default_factory=list)

    @classmethod
    def default(cls, description: str = "") -> "AnalysisResult":
        """Create a default analysis result for fallback scenarios."""
        return cls(
            framework="HTML/CSS/JS",
            requirements=description,
        )
