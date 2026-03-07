import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from backup_manager import BackupManager

class TestBackupManager(unittest.TestCase):

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.unlink')
    def test_delete_backup_success(self, mock_unlink, mock_exists):
        manager = BackupManager(backup_dir="/tmp/test_backups")
        mock_exists.return_value = True

        result = manager.delete_backup("backup_20230101_120000.json")

        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Deleted backup: backup_20230101_120000.json")
        mock_unlink.assert_called_once()
        mock_exists.assert_called_once()

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.unlink')
    def test_delete_backup_not_found(self, mock_unlink, mock_exists):
        manager = BackupManager(backup_dir="/tmp/test_backups")
        mock_exists.return_value = False

        result = manager.delete_backup("backup_missing.json")

        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Backup not found: backup_missing.json")
        mock_unlink.assert_not_called()
        mock_exists.assert_called_once()

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.unlink')
    def test_delete_backup_exception(self, mock_unlink, mock_exists):
        manager = BackupManager(backup_dir="/tmp/test_backups")
        mock_exists.return_value = True
        mock_unlink.side_effect = Exception("Permission denied")

        result = manager.delete_backup("backup_error.json")

        self.assertFalse(result['success'])
        self.assertTrue("Failed to delete backup" in result['message'])
        mock_unlink.assert_called_once()

if __name__ == '__main__':
    unittest.main()
