import unittest
from unittest.mock import patch, MagicMock
from adb_operations import ADBOperations, ADBError

class TestADBOperations(unittest.TestCase):
    def setUp(self):
        self.adb = ADBOperations()

    @patch.object(ADBOperations, '_run_command')
    def test_uninstall_package_success(self, mock_run_command):
        mock_run_command.return_value = "Success\n"
        result = self.adb.uninstall_package("com.example.app")

        mock_run_command.assert_called_once_with(
            [self.adb.adb_path, "shell", "pm", "uninstall", "--user", "0", "com.example.app"]
        )
        self.assertEqual(result, {
            "success": True,
            "message": "Successfully uninstalled com.example.app"
        })

    @patch.object(ADBOperations, '_run_command')
    def test_uninstall_package_failure(self, mock_run_command):
        mock_run_command.return_value = "Failure [DELETE_FAILED_INTERNAL_ERROR]\n"
        result = self.adb.uninstall_package("com.example.app")

        mock_run_command.assert_called_once_with(
            [self.adb.adb_path, "shell", "pm", "uninstall", "--user", "0", "com.example.app"]
        )
        self.assertEqual(result, {
            "success": False,
            "message": "Failed to uninstall: Failure [DELETE_FAILED_INTERNAL_ERROR]"
        })

    @patch.object(ADBOperations, '_run_command')
    def test_uninstall_package_exception(self, mock_run_command):
        mock_run_command.side_effect = Exception("ADB command failed")
        result = self.adb.uninstall_package("com.example.app")

        mock_run_command.assert_called_once_with(
            [self.adb.adb_path, "shell", "pm", "uninstall", "--user", "0", "com.example.app"]
        )
        self.assertEqual(result, {
            "success": False,
            "message": "ADB command failed"
        })

if __name__ == '__main__':
    unittest.main()
