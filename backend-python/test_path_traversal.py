import sys
from pathlib import Path

# Add backend-python to sys.path so we can import backup_manager properly
sys.path.insert(0, str(Path(__file__).parent))
from backup_manager import BackupManager

def test_path_traversal():
    bm = BackupManager("/tmp/backups")
    bm.backup_dir.mkdir(parents=True, exist_ok=True)

    # Create a sensitive file
    sensitive_file = Path("/tmp/sensitive.txt")
    sensitive_file.write_text("secret")

    print("Testing delete_backup with path traversal...")
    res = bm.delete_backup("../sensitive.txt")
    print(res)

    if sensitive_file.exists():
        print("Sensitive file still exists. Protected!")
        sensitive_file.unlink() # Cleanup
        return 0
    else:
        print("VULNERABILITY: Sensitive file was deleted!")
        return 1

if __name__ == '__main__':
    sys.exit(test_path_traversal())
