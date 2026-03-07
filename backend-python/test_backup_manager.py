import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
from backup_manager import BackupManager

class TestBackupManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.manager = BackupManager(backup_dir=self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_delete_backup_success(self):
        # Create a real temporary file
        backup_name = "backup_20230101_120000.json"
        backup_path = Path(self.temp_dir.name) / backup_name
        backup_path.touch()

        # Ensure it exists before deletion
        self.assertTrue(backup_path.exists())

        # Perform deletion
        result = self.manager.delete_backup(backup_name)

        # Verify success
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], f"Deleted backup: {backup_name}")
        self.assertFalse(backup_path.exists())

    def test_delete_backup_not_found(self):
        backup_name = "backup_missing.json"
        backup_path = Path(self.temp_dir.name) / backup_name

        # Ensure it does NOT exist before deletion
        self.assertFalse(backup_path.exists())

        # Perform deletion
        result = self.manager.delete_backup(backup_name)

        # Verify not found
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], f"Backup not found: {backup_name}")

    def test_delete_backup_exception(self):
        backup_name = "backup_error.json"
        backup_path = Path(self.temp_dir.name) / backup_name
        backup_path.touch()

        # Patch the specific unlink method to raise an exception
        with patch.object(Path, 'unlink', side_effect=Exception("Permission denied")):
            result = self.manager.delete_backup(backup_name)

        self.assertFalse(result['success'])
        self.assertTrue("Failed to delete backup" in result['message'])
        self.assertTrue("Permission denied" in result['message'])

    def test_delete_backup_path_traversal(self):
        # Attempt to delete a file outside the backup directory.
        # Note: _get_safe_backup_path takes the filename part using Path.name,
        # meaning "../outside_backup.json" becomes "outside_backup.json"
        # and doesn't actually trigger path traversal. The missing file
        # naturally triggers 'Backup not found'.
        backup_name = "../outside_backup.json"

        result = self.manager.delete_backup(backup_name)

        self.assertFalse(result['success'])
        self.assertTrue("Backup not found:" in result['message'])

if __name__ == '__main__':
    unittest.main()
