from unittest.mock import MagicMock
import pytest
from ismk.persistence import Persistence

@pytest.fixture
def persistence(tmp_path):
    mock_dag = MagicMock()
    mock_dag.workflow.dag_settings.max_checksum_file_size = 1000
    # Mock other needed attributes if any
    
    p = Persistence(dag=mock_dag, path=tmp_path / ".ismk")
    return p

def test_backup_restore_file(persistence, tmp_path):
    # Create a dummy file
    f = tmp_path / "output.txt"
    f.write_text("original content")
    
    # Backup
    persistence.backup_output(f)
    
    # Check backup exists
    backup_file = persistence._get_backup_path(f)
    assert backup_file.exists()
    assert backup_file.read_text() == "original content"
    
    # Modify original
    f.write_text("modified content")
    
    # Restore
    persistence.restore_output(f)
    assert f.read_text() == "original content"
    # Restore should delete backup
    assert not backup_file.exists()

def test_backup_restore_directory(persistence, tmp_path):
    d = tmp_path / "output_dir"
    d.mkdir()
    (d / "file1.txt").write_text("content1")
    
    # Backup
    persistence.backup_output(d)
    
    backup_dir = persistence._get_backup_path(d)
    assert backup_dir.exists()
    assert backup_dir.is_dir()
    assert (backup_dir / "file1.txt").read_text() == "content1"
    
    # Modify
    (d / "file1.txt").write_text("modified")
    (d / "file2.txt").write_text("new file")
    
    # Restore
    persistence.restore_output(d)
    
    assert (d / "file1.txt").read_text() == "content1"
    assert not (d / "file2.txt").exists()
    assert not backup_dir.exists()

def test_cleanup_backup(persistence, tmp_path):
    f = tmp_path / "output.txt"
    f.write_text("content")
    
    persistence.backup_output(f)
    backup_file = persistence._get_backup_path(f)
    assert backup_file.exists()
    
    persistence.cleanup_backup(f)
    assert not backup_file.exists()

def test_restore_no_backup(persistence, tmp_path):
    f = tmp_path / "missing.txt"
    result = persistence.restore_output(f)
    assert result is False
