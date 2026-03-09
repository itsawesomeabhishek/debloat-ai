import os
import tempfile
from pathlib import Path
from backup_manager import BackupManager

def test_path_traversal():
    print("Testing BackupManager for path traversal vulnerability...")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a "sensitive" file outside the backup directory
        sensitive_file_path = Path(temp_dir) / "sensitive_data.txt"
        with open(sensitive_file_path, "w") as f:
            f.write("SECRET_KEY_123")

        # Initialize BackupManager with a subdirectory as the backup dir
        backup_dir = Path(temp_dir) / "backups"
        backup_manager = BackupManager(str(backup_dir))

        # Test 1: Attempt to read the sensitive file using traversal
        traversal_path = "../sensitive_data.txt"
        print(f"\nAttempting to restore from: {traversal_path}")

        # In a vulnerable version, this might read the file or throw a JSON decode error
        # In the fixed version, the path should be constrained to the backup dir
        result = backup_manager.restore_backup(traversal_path)

        print(f"Result: {result}")
        if result.get("success") == False and "Failed to restore backup:" in result.get("message", ""):
            # We want to know if it's the expected ValueError or something else
            print("Traversed attempt caught by exception!")
        elif result.get("success") == False and "Backup not found" in result.get("message", ""):
            print("Path was neutralized (interpreted as just 'sensitive_data.txt' inside backup dir)!")

        # Check if the path resolved inside the backup directory
        safe_path = backup_dir / "sensitive_data.txt"
        if not safe_path.exists():
            print(f"File {safe_path} does not exist, which is expected since it was neutralized.")

        # Test 2: Attempt to delete the sensitive file using traversal
        print(f"\nAttempting to delete from: {traversal_path}")
        del_result = backup_manager.delete_backup(traversal_path)
        print(f"Delete Result: {del_result}")

        if sensitive_file_path.exists():
            print("SUCCESS: Sensitive file was NOT deleted!")
        else:
            print("FAILURE: Sensitive file WAS deleted!")

if __name__ == "__main__":
    test_path_traversal()
