"""
MultiAgent Developer - Backlog Card Processor
Entry point for the application.
"""
import sys
import logging
from pathlib import Path
from typing import Optional

from core.config import load_settings, setup_logging, Settings
from core.entities import BacklogCard
from core.exceptions import ConfigurationError, ParsingError
from core.orchestrator import BacklogOrchestrator
from core.parsers import BacklogCardParser


class CLI:
    """Command-line interface for the application."""
    
    FORMAT_HINTS = {
        "1": "json",
        "2": "markdown", 
        "3": "plain_text",
        "4": None,
    }
    
    def __init__(self, settings: Settings, logger: logging.Logger):
        self._settings = settings
        self._logger = logger
        self._parser = BacklogCardParser()
    
    def run(self) -> int:
        """Main entry point. Returns exit code."""
        try:
            self._print_header()
            
            project_path = self._get_project_path()
            card_data, format_hint = self._get_card_input()
            card = self._parse_card(card_data, format_hint)
            
            self._print_card_summary(card)
            
            if not self._confirm_execution():
                self._logger.info("Execution cancelled by user")
                return 0
            
            result = self._execute(card, project_path)
            self._handle_result(result, card)
            
            return 0
            
        except KeyboardInterrupt:
            self._logger.info("Interrupted by user")
            return 130
        except Exception as e:
            self._logger.error(f"Execution failed: {e}")
            return 1
    
    def _print_header(self) -> None:
        print("\n" + "=" * 60)
        print("MultiAgent Developer - Backlog Card Processor")
        print("=" * 60)
        print("\nSupported formats: JSON, Markdown, Plain text")
        print("-" * 60)
    
    def _get_project_path(self) -> str:
        path = input("\nProject path (default: current directory): ").strip()
        return path if path else "."
    
    def _get_card_input(self) -> tuple[str, Optional[str]]:
        print("\nHow would you like to provide the backlog card?")
        print("1. Type/paste directly")
        print("2. Read from file")
        
        choice = input("\nSelect option (1-2): ").strip()
        
        if choice == "1":
            return self._get_direct_input()
        elif choice == "2":
            return self._get_file_input()
        else:
            raise ValueError("Invalid option selected")
    
    def _get_direct_input(self) -> tuple[str, Optional[str]]:
        print("\nPaste your backlog card (type 'END' on a new line when finished):")
        
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        
        print("\nFormat hint (optional):")
        print("1. JSON  2. Markdown  3. Plain text  4. Auto-detect")
        fmt_choice = input("Select format (1-4, default: 4): ").strip()
        
        return "\n".join(lines), self.FORMAT_HINTS.get(fmt_choice)
    
    def _get_file_input(self) -> tuple[str, Optional[str]]:
        file_path = input("\nEnter file path: ").strip()
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = path.read_text(encoding="utf-8")
        self._logger.info(f"Read file: {file_path}")
        
        format_hint = None
        if path.suffix == ".json":
            format_hint = "json"
        elif path.suffix == ".md":
            format_hint = "markdown"
        
        return content, format_hint
    
    def _parse_card(self, data: str, format_hint: Optional[str]) -> BacklogCard:
        self._logger.info("Parsing backlog card")
        return self._parser.parse(data, format_hint)
    
    def _print_card_summary(self, card: BacklogCard) -> None:
        print(f"\nCard Summary:")
        print(f"  Title: {card.title}")
        print(f"  Priority: {card.priority or 'Not set'}")
        print(f"  Story Points: {card.story_points or 'Not set'}")
        print(f"  Acceptance Criteria: {len(card.acceptance_criteria)} items")
    
    def _confirm_execution(self) -> bool:
        response = input("\nReady to process? (y/N): ").strip().lower()
        return response == "y"
    
    def _execute(self, card: BacklogCard, project_path: str) -> str:
        print("\n" + "=" * 60)
        print("Processing backlog card...")
        print("=" * 60 + "\n")
        
        orchestrator = BacklogOrchestrator(card, project_path, self._settings)
        return orchestrator.execute()
    
    def _handle_result(self, result: str, card: BacklogCard) -> None:
        print("\n" + "=" * 60)
        print("PROCESSING COMPLETE")
        print("=" * 60)
        
        output_file = input("\nSave result to file? (press Enter for 'result.md'): ").strip()
        if not output_file:
            output_file = "result.md"
        
        self._save_result(output_file, result, card)
    
    def _save_result(self, filename: str, result: str, card: BacklogCard) -> None:
        try:
            content = f"# Backlog Card Processing Result\n\n"
            content += f"## Original Card\n\n{card.to_markdown()}\n"
            content += f"## Implementation Result\n\n{result}"
            
            Path(filename).write_text(content, encoding="utf-8")
            self._logger.info(f"Result saved to: {filename}")
            print(f"Result saved to: {filename}")
        except IOError as e:
            self._logger.warning(f"Could not save file: {e}")


def validate_configuration(settings: Settings) -> None:
    """Validate required configuration."""
    if not settings.openai_api_key:
        raise ConfigurationError(
            "OPENAI_API_KEY not found. Please set up your .env file."
        )


def main() -> int:
    """Application entry point."""
    import warnings
    warnings.filterwarnings("ignore")
    
    try:
        settings = load_settings()
        validate_configuration(settings)
        logger = setup_logging(settings.log_level)
        
        cli = CLI(settings, logger)
        return cli.run()
        
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
