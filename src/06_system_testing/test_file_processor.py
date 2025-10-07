"""
Tests for FileProcessor using temporary files and directories.
"""
import pytest
from pathlib import Path
from file_processor import FileProcessor

def test_create_backup(tmp_path):
    """Test backup creation with temporary files."""
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    # Create backup
    processor = FileProcessor(tmp_path)
    backup_file = processor.create_backup(test_file)
    
    # Verify backup
    assert backup_file.exists()
    assert backup_file.suffix == ".txt.bak"
    assert backup_file.read_text() == "test content"

def test_count_lines(tmp_path):
    """Test line counting with temporary files."""
    # Create test file with multiple lines
    test_file = tmp_path / "multiline.txt"
    test_file.write_text("line 1\nline 2\nline 3\n")
    
    processor = FileProcessor()
    assert processor.count_lines(test_file) == 3

def test_merge_files(tmp_path):
    """Test file merging with temporary files."""
    # Create test files
    files = []
    for i in range(3):
        file = tmp_path / f"part{i}.txt"
        file.write_text(f"content {i}")
        files.append(file)
    
    # Merge files
    output_file = tmp_path / "merged.txt"
    processor = FileProcessor()
    processor.merge_files(files, output_file)
    
    # Verify merged content
    content = output_file.read_text()
    assert "content 0" in content
    assert "content 1" in content
    assert "content 2" in content

def test_search_content(tmp_path):
    """Test content searching in temporary directory."""
    # Create test files with different content
    (tmp_path / "file1.txt").write_text("contains target text")
    (tmp_path / "file2.txt").write_text("different content")
    
    # Create subdirectory with files
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file3.txt").write_text("more target text")
    
    processor = FileProcessor()
    matches = processor.search_content(tmp_path, "target")
    
    assert len(matches) == 2
    assert any(file.name == "file1.txt" for file in matches)
    assert any(file.name == "file3.txt" for file in matches)

def test_file_not_found(tmp_path):
    """Test error handling for non-existent files."""
    processor = FileProcessor()
    non_existent = tmp_path / "doesnotexist.txt"
    
    with pytest.raises(FileNotFoundError):
        processor.count_lines(non_existent)

def test_merge_no_files(tmp_path):
    """Test error handling when no files provided for merge."""
    processor = FileProcessor()
    output_file = tmp_path / "output.txt"
    
    with pytest.raises(ValueError, match="No input files provided"):
        processor.merge_files([], output_file)