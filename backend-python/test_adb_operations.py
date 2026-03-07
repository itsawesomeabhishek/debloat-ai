import unittest
from unittest.mock import MagicMock
from adb_operations import ADBOperations

class TestADBOperations(unittest.TestCase):

    def setUp(self):
        self.adb = ADBOperations()
        self.adb.adb_path = "mock_adb"
        self.adb._run_command = MagicMock()

    def test_reinstall_package_success(self):
        self.adb._run_command.return_value = "Package com.example.app installed for user: 0"
        result = self.adb.reinstall_package("com.example.app")

        self.adb._run_command.assert_called_once_with(
            ["mock_adb", "shell", "cmd", "package", "install-existing", "com.example.app"]
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Successfully reinstalled com.example.app")

    def test_reinstall_package_failure(self):
        self.adb._run_command.return_value = "Failure [INSTALL_FAILED_INVALID_URI]"
        result = self.adb.reinstall_package("com.example.app")

        self.adb._run_command.assert_called_once_with(
            ["mock_adb", "shell", "cmd", "package", "install-existing", "com.example.app"]
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Failed to reinstall: Failure [INSTALL_FAILED_INVALID_URI]")

    def test_reinstall_package_exception(self):
        self.adb._run_command.side_effect = Exception("ADB connection lost")
        result = self.adb.reinstall_package("com.example.app")

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "ADB connection lost")

if __name__ == '__main__':
    unittest.main()
