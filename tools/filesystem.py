"""
Filesystem tools for file and directory operations.
"""
import os
from pathlib import Path

from langchain.tools import tool


class FileSystemTools:
    """Collection of filesystem operation tools."""
    
    @staticmethod
    @tool("Write file")
    def write_file(filename: str, content: str) -> str:
        """Write content to a file. Creates parent directories if needed."""
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"File '{filename}' written successfully."
    
    @staticmethod
    @tool("Create directory")
    def create_directory(directory_path: str) -> str:
        """Create a directory and any necessary parent directories."""
        path = Path(directory_path)
        if path.exists():
            return f"Directory '{directory_path}' already exists."
        path.mkdir(parents=True, exist_ok=True)
        return f"Directory '{directory_path}' created successfully."


# Backward compatibility aliases
class FileWriteTool:
    file_write_tool = FileSystemTools.write_file


class DirWriteTool:
    dir_write_tool = FileSystemTools.create_directory
