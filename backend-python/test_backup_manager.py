import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import os
import sys
import json
from datetime import datetime

# Ensure we can import backup_manager
sys.path.insert(0, os.path.dirname(__file__))

from backup_manager import BackupManager

class TestBackupManagerCreateBackup(unittest.TestCase):

    def setUp(self):
        # Prevent BackupManager from creating actual directories during tests
        with patch.object(Path, 'mkdir'):
            self.bm = BackupManager(backup_dir="/mock/backup/dir")

    @patch('backup_manager.datetime')
    @patch('backup_manager.json.dump')
    def test_create_backup_success(self, mock_json_dump, mock_datetime):
        # Arrange
        mock_now = datetime(2023, 10, 27, 12, 34, 56)
        mock_datetime.now.return_value = mock_now

        packages = ["com.test.app1", "com.test.app2"]
        device_info = {"model": "TestPhone"}

        expected_backup_name = "backup_20231027_123456.json"
        expected_backup_path = Path("/mock/backup/dir") / expected_backup_name

        m_open = mock_open()
        with patch('builtins.open', m_open):
            # Act
            result = self.bm.create_backup(packages, device_info)

            # Assert
            self.assertTrue(result['success'])
            self.assertEqual(result['backupName'], expected_backup_name)
            self.assertEqual(result['backupPath'], str(expected_backup_path))
            self.assertEqual(result['message'], f"Backup created: {expected_backup_name}")

            # Check file was opened correctly
            m_open.assert_called_once_with(expected_backup_path, 'w', encoding='utf-8')

            # Check json.dump was called with correct data
            mock_json_dump.assert_called_once()
            args, kwargs = mock_json_dump.call_args
            backup_data = args[0]
            self.assertEqual(backup_data["timestamp"], mock_now.isoformat())
            self.assertEqual(backup_data["deviceInfo"], device_info)
            self.assertEqual(backup_data["packages"], packages)
            self.assertEqual(backup_data["count"], 2)

            self.assertEqual(kwargs['indent'], 2)
            self.assertEqual(kwargs['ensure_ascii'], False)

    @patch('backup_manager.datetime')
    def test_create_backup_no_device_info(self, mock_datetime):
        # Arrange
        mock_now = datetime(2023, 10, 27, 12, 34, 56)
        mock_datetime.now.return_value = mock_now

        packages = ["com.test.app1"]

        m_open = mock_open()
        with patch('builtins.open', m_open), patch('backup_manager.json.dump') as mock_json_dump:
            # Act - don't pass device_info
            result = self.bm.create_backup(packages)

            # Assert
            self.assertTrue(result['success'])

            # Check json.dump was called with correct data, deviceInfo should be {}
            args, _ = mock_json_dump.call_args
            backup_data = args[0]
            self.assertEqual(backup_data["deviceInfo"], {})

    @patch('backup_manager.datetime')
    def test_create_backup_handles_exception(self, mock_datetime):
        # Arrange
        mock_now = datetime(2023, 10, 27, 12, 34, 56)
        mock_datetime.now.return_value = mock_now

        packages = ["com.test.app1"]

        # Make open raise an exception (e.g., PermissionError)
        m_open = mock_open()
        m_open.side_effect = PermissionError("Permission denied")

        with patch('builtins.open', m_open):
            # Act
            result = self.bm.create_backup(packages)

            # Assert
            self.assertFalse(result['success'])
            self.assertIn("Failed to create backup: Permission denied", result['message'])

if __name__ == '__main__':
    unittest.main()
