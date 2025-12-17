"""
Backlog card parsers following Single Responsibility Principle.
Each parser handles one specific format.
"""
import json
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from .entities import BacklogCard
from .exceptions import ParsingError


class BaseParser(ABC):
    """Abstract base parser - Template Method pattern."""
    
    @abstractmethod
    def parse(self, data: str) -> BacklogCard:
        """Parse raw data into a BacklogCard."""
        pass
    
    @abstractmethod
    def can_parse(self, data: str) -> bool:
        """Check if this parser can handle the given data."""
        pass


class JsonParser(BaseParser):
    """Parser for JSON format backlog cards (including JIRA API)."""
    
    JIRA_STORY_POINTS_FIELDS = [
        "customfield_10002", 
        "customfield_10004", 
        "story points", 
        "Story Points"
    ]
    
    EXCLUDED_JIRA_FIELDS = {
        "summary", "description", "priority", 
        "labels", "assignee", "reporter", "duedate"
    }
    
    EXCLUDED_GENERIC_FIELDS = {
        "title", "name", "description", "acceptance_criteria",
        "priority", "story_points", "labels", "assignee", "reporter"
    }
    
    def can_parse(self, data: str) -> bool:
        data = data.strip()
        return data.startswith("{") and data.endswith("}")
    
    def parse(self, data: str) -> BacklogCard:
        try:
            card_data = json.loads(data)
        except json.JSONDecodeError as e:
            raise ParsingError(f"Invalid JSON: {e}")
        
        if "fields" in card_data:
            return self._parse_jira_format(card_data["fields"])
        return self._parse_generic_format(card_data)
    
    def _parse_jira_format(self, fields: Dict) -> BacklogCard:
        return BacklogCard(
            title=fields.get("summary", ""),
            description=fields.get("description", ""),
            acceptance_criteria=self._extract_ac_from_description(
                fields.get("description", "")
            ),
            priority=self._get_nested(fields, "priority", "name"),
            story_points=self._extract_story_points(fields),
            labels=list(fields.get("labels", [])),
            assignee=self._get_nested(fields, "assignee", "displayName"),
            reporter=self._get_nested(fields, "reporter", "displayName"),
            due_date=self._parse_date(fields.get("duedate")),
            custom_fields={
                k: v for k, v in fields.items() 
                if k not in self.EXCLUDED_JIRA_FIELDS
            },
            original_format="jira_api",
        )
    
    def _parse_generic_format(self, data: Dict) -> BacklogCard:
        return BacklogCard(
            title=data.get("title", data.get("name", "")),
            description=data.get("description", ""),
            acceptance_criteria=data.get("acceptance_criteria", []),
            priority=data.get("priority"),
            story_points=data.get("story_points"),
            labels=data.get("labels", []),
            assignee=data.get("assignee"),
            reporter=data.get("reporter"),
            custom_fields={
                k: v for k, v in data.items() 
                if k not in self.EXCLUDED_GENERIC_FIELDS
            },
            original_format="json",
        )
    
    def _get_nested(self, data: Dict, key: str, nested_key: str) -> Optional[str]:
        value = data.get(key)
        if isinstance(value, dict):
            return value.get(nested_key)
        return None
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            return None
    
    def _extract_story_points(self, fields: Dict) -> Optional[int]:
        for field_name in self.JIRA_STORY_POINTS_FIELDS:
            if field_name in fields:
                try:
                    return int(fields[field_name])
                except (ValueError, TypeError):
                    continue
        return None
    
    def _extract_ac_from_description(self, description: str) -> List[str]:
        if not description:
            return []
        
        ac_list = []
        in_ac_section = False
        
        for line in description.split("\n"):
            line_lower = line.lower().strip()
            
            if "acceptance criteria" in line_lower or line_lower.startswith("ac:"):
                in_ac_section = True
                continue
            
            if in_ac_section:
                stripped = line.strip()
                if stripped.startswith("-") or stripped.startswith("*"):
                    ac_list.append(stripped[1:].strip())
                elif stripped:
                    in_ac_section = False
        
        return ac_list


class MarkdownParser(BaseParser):
    """Parser for Markdown format backlog cards."""
    
    AC_SECTION_HEADERS = {"## Acceptance Criteria", "## AC"}
    
    def can_parse(self, data: str) -> bool:
        return data.strip().startswith("# ")
    
    def parse(self, data: str) -> BacklogCard:
        lines = data.strip().split("\n")
        
        title = self._extract_title(lines)
        description, acceptance_criteria = self._extract_sections(lines)
        metadata = self._extract_metadata(lines)
        
        return BacklogCard(
            title=title,
            description=description,
            acceptance_criteria=acceptance_criteria,
            priority=metadata.get("priority"),
            story_points=metadata.get("story_points"),
            labels=metadata.get("labels", []),
            assignee=metadata.get("assignee"),
            original_format="markdown",
        )
    
    def _extract_title(self, lines: List[str]) -> str:
        for line in lines:
            if line.startswith("# "):
                return line[2:].strip()
        return ""
    
    def _extract_sections(self, lines: List[str]) -> tuple:
        description = []
        acceptance_criteria = []
        current_section = "description"
        
        for line in lines:
            if line.startswith("# "):
                continue
            elif any(line.startswith(header) for header in self.AC_SECTION_HEADERS):
                current_section = "acceptance_criteria"
            elif line.startswith("##"):
                current_section = "other"
            elif line.startswith("- ") or line.startswith("* "):
                if current_section == "acceptance_criteria":
                    acceptance_criteria.append(line[2:].strip())
            elif current_section == "description" and line.strip():
                if not self._is_metadata_line(line):
                    description.append(line.strip())
        
        return "\n".join(description), acceptance_criteria
    
    def _extract_metadata(self, lines: List[str]) -> Dict:
        metadata = {}
        
        for line in lines:
            line_lower = line.lower()
            
            if line_lower.startswith("priority:"):
                metadata["priority"] = line.split(":", 1)[1].strip()
            elif line_lower.startswith("story points:"):
                try:
                    metadata["story_points"] = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
            elif line_lower.startswith("labels:"):
                metadata["labels"] = [
                    l.strip() for l in line.split(":", 1)[1].split(",")
                ]
            elif line_lower.startswith("assignee:"):
                metadata["assignee"] = line.split(":", 1)[1].strip()
        
        return metadata
    
    def _is_metadata_line(self, line: str) -> bool:
        prefixes = ("priority:", "story points:", "labels:", "assignee:")
        return line.lower().startswith(prefixes)


class PlainTextParser(BaseParser):
    """Parser for plain text backlog cards."""
    
    AC_PATTERN = re.compile(
        r"^\s*[-*]\s*(.+)|^\s*\d+\.\s*(.+)|^AC:\s*(.+)", 
        re.IGNORECASE
    )
    
    def can_parse(self, data: str) -> bool:
        return True  # Fallback parser
    
    def parse(self, data: str) -> BacklogCard:
        lines = data.strip().split("\n")
        
        title = lines[0] if lines else ""
        description = []
        acceptance_criteria = []
        metadata = {}
        
        current_section = "description"
        
        for line in lines[1:]:
            ac_match = self.AC_PATTERN.match(line)
            
            if ac_match:
                current_section = "acceptance_criteria"
                ac_text = next(filter(None, ac_match.groups()))
                acceptance_criteria.append(ac_text.strip())
            elif self._extract_metadata_from_line(line, metadata):
                continue
            elif current_section == "description":
                description.append(line.strip())
        
        return BacklogCard(
            title=title,
            description="\n".join(description),
            acceptance_criteria=acceptance_criteria,
            priority=metadata.get("priority"),
            story_points=metadata.get("story_points"),
            labels=metadata.get("labels", []),
            assignee=metadata.get("assignee"),
            original_format="plain_text",
        )
    
    def _extract_metadata_from_line(self, line: str, metadata: Dict) -> bool:
        line_lower = line.lower()
        
        if line_lower.startswith("priority:"):
            metadata["priority"] = line.split(":", 1)[1].strip()
            return True
        elif line_lower.startswith("story points:"):
            try:
                metadata["story_points"] = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
            return True
        elif line_lower.startswith("assignee:"):
            metadata["assignee"] = line.split(":", 1)[1].strip()
            return True
        elif line_lower.startswith("labels:"):
            metadata["labels"] = [
                l.strip() for l in line.split(":", 1)[1].split(",")
            ]
            return True
        
        return False


class BacklogCardParser:
    """
    Facade for parsing backlog cards.
    Uses Strategy pattern to delegate to appropriate parser.
    """
    
    def __init__(self):
        self._parsers = [
            JsonParser(),
            MarkdownParser(),
            PlainTextParser(),
        ]
    
    def parse(self, data: str, format_hint: Optional[str] = None) -> BacklogCard:
        """Parse data into a BacklogCard using auto-detection or hint."""
        data = data.strip()
        
        if format_hint:
            parser = self._get_parser_by_hint(format_hint.lower())
            if parser:
                return parser.parse(data)
        
        for parser in self._parsers:
            if parser.can_parse(data):
                return parser.parse(data)
        
        raise ParsingError("Unable to parse backlog card data")
    
    def _get_parser_by_hint(self, hint: str) -> Optional[BaseParser]:
        hint_map = {
            "json": JsonParser,
            "markdown": MarkdownParser,
            "plain_text": PlainTextParser,
        }
        parser_class = hint_map.get(hint)
        return parser_class() if parser_class else None
