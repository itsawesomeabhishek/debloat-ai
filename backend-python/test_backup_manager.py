import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import json

from backup_manager import BackupManager

class TestBackupManager(unittest.TestCase):
    def setUp(self):
        # Prevent actual directory creation during test setup
        with patch('pathlib.Path.mkdir'):
            self.manager = BackupManager("/fake/backup/dir")

    @patch('pathlib.Path.glob')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_backups_success(self, mock_json_load, mock_file, mock_glob):
        """Test listing backups successfully and sorting by timestamp"""
        # Mock glob to return two files
        file1 = MagicMock(spec=Path)
        file1.name = "backup_20230101_120000.json"
        file1.__str__.return_value = "/fake/backup/dir/backup_20230101_120000.json"

        file2 = MagicMock(spec=Path)
        file2.name = "backup_20230102_120000.json"
        file2.__str__.return_value = "/fake/backup/dir/backup_20230102_120000.json"

        mock_glob.return_value = [file1, file2]

        # Mock json.load to return different data for each file
        data1 = {
            "timestamp": "2023-01-01T12:00:00",
            "count": 2,
            "deviceInfo": {"model": "Device1"}
        }
        data2 = {
            "timestamp": "2023-01-02T12:00:00",
            "count": 5,
            "deviceInfo": {"model": "Device2"}
        }
        # First file1 is loaded, then file2 is loaded
        mock_json_load.side_effect = [data1, data2]

        backups = self.manager.list_backups()

        # Should be sorted by timestamp, newest first (data2 then data1)
        self.assertEqual(len(backups), 2)

        # Check newest file is first
        self.assertEqual(backups[0]["name"], "backup_20230102_120000.json")
        self.assertEqual(backups[0]["path"], "/fake/backup/dir/backup_20230102_120000.json")
        self.assertEqual(backups[0]["timestamp"], "2023-01-02T12:00:00")
        self.assertEqual(backups[0]["packageCount"], 5)
        self.assertEqual(backups[0]["deviceInfo"], {"model": "Device2"})

        # Check oldest file is second
        self.assertEqual(backups[1]["name"], "backup_20230101_120000.json")
        self.assertEqual(backups[1]["path"], "/fake/backup/dir/backup_20230101_120000.json")
        self.assertEqual(backups[1]["timestamp"], "2023-01-01T12:00:00")
        self.assertEqual(backups[1]["packageCount"], 2)
        self.assertEqual(backups[1]["deviceInfo"], {"model": "Device1"})

    @patch('pathlib.Path.glob')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_list_backups_corrupted(self, mock_json_load, mock_file, mock_glob):
        """Test listing backups when one file is corrupted"""
        # Mock glob to return two files
        file1 = MagicMock(spec=Path)
        file1.name = "backup_good.json"
        file1.__str__.return_value = "/fake/backup/dir/backup_good.json"

        file2 = MagicMock(spec=Path)
        file2.name = "backup_corrupted.json"
        file2.__str__.return_value = "/fake/backup/dir/backup_corrupted.json"

        mock_glob.return_value = [file1, file2]

        # First file succeeds, second file throws an exception
        data1 = {
            "timestamp": "2023-01-01T12:00:00",
            "count": 2,
            "deviceInfo": {"model": "Device1"}
        }
        mock_json_load.side_effect = [data1, Exception("Corrupted JSON")]

        backups = self.manager.list_backups()

        # Should only contain the good file and not raise exception
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0]["name"], "backup_good.json")

    @patch('pathlib.Path.glob')
    def test_list_backups_exception(self, mock_glob):
        """Test list_backups raises exception correctly on main failure"""
        # Simulate an exception in glob
        mock_glob.side_effect = Exception("Glob failure")

        with self.assertRaises(Exception) as context:
            self.manager.list_backups()

        self.assertTrue(str(context.exception).startswith("Failed to list backups:"))
        self.assertIn("Glob failure", str(context.exception))

if __name__ == '__main__':
    unittest.main()
