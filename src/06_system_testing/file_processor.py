"""
File processing utility demonstrating temporary file handling.
"""
import os
from pathlib import Path
from typing import List, Optional

class FileProcessor:
    """Class for processing files with various operations."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize with optional base directory."""
        self.base_dir = base_dir or Path.cwd()
    
    def create_backup(self, file_path: Path) -> Path:
        """Create a backup of a file with .bak extension."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        backup_path.write_bytes(file_path.read_bytes())
        return backup_path
    
    def count_lines(self, file_path: Path) -> int:
        """Count number of lines in a file."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return sum(1 for _ in file_path.open())
    
    def merge_files(self, files: List[Path], output_file: Path) -> None:
        """Merge multiple files into one."""
        if not files:
            raise ValueError("No input files provided")
        
        with output_file.open('w') as out:
            for file in files:
                if not file.exists():
                    raise FileNotFoundError(f"File not found: {file}")
                out.write(file.read_text())
                out.write('\n')
    
    def search_content(self, directory: Path, pattern: str) -> List[Path]:
        """Search for files containing the given pattern."""
        if not directory.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory}")
        
        matches = []
        for file in directory.glob('**/*'):
            if file.is_file():
                try:
                    if pattern in file.read_text():
                        matches.append(file)
                except (PermissionError, UnicodeDecodeError):
                    continue
        return matches