import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
from backup_manager import BackupManager

class TestBackupManager(unittest.TestCase):

    @patch('pathlib.Path.exists')
    def test_restore_backup_success(self, mock_exists):
        manager = BackupManager(backup_dir="/tmp/test_backups")
        mock_exists.return_value = True

        with patch('builtins.open', mock_open(read_data='{"packages": ["pkg1", "pkg2"]}')) as mock_file:
            result = manager.restore_backup("backup_20230101_120000.json")

            self.assertTrue(result['success'])
            self.assertEqual(result['packages'], ["pkg1", "pkg2"])
            self.assertEqual(result['count'], 2)
            self.assertEqual(result['message'], "Loaded 2 packages from backup")
            mock_exists.assert_called_once()
            mock_file.assert_called_once()

    @patch('pathlib.Path.exists')
    def test_restore_backup_not_found(self, mock_exists):
        manager = BackupManager(backup_dir="/tmp/test_backups")
        mock_exists.return_value = False

        result = manager.restore_backup("backup_missing.json")

        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Backup not found: backup_missing.json")
        mock_exists.assert_called_once()

    @patch('pathlib.Path.exists')
    def test_restore_backup_exception(self, mock_exists):
        manager = BackupManager(backup_dir="/tmp/test_backups")
        mock_exists.return_value = True

        with patch('builtins.open') as mock_file:
            mock_file.side_effect = Exception("File read error")
            result = manager.restore_backup("backup_error.json")

            self.assertFalse(result['success'])
            self.assertEqual(result['message'], "Failed to restore backup: File read error")
            mock_exists.assert_called_once()
            mock_file.assert_called_once()

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
