import unittest
from unittest.mock import patch, MagicMock
from adb_operations import ADBOperations, ADBError

class TestADBOperationsSecurity(unittest.TestCase):
    def setUp(self):
        self.adb = ADBOperations()

    def test_is_valid_package_name_valid(self):
        valid_names = [
            "com.example.app",
            "com.android.systemui",
            "android",
            "a.b.c",
            "com.example_app.v1"
        ]
        for name in valid_names:
            self.assertTrue(ADBOperations.is_valid_package_name(name), f"Should be valid: {name}")

    def test_is_valid_package_name_invalid(self):
        invalid_names = [
            "com.example; rm -rf /",
            "com.example&&ls",
            "com.example|grep",
            "com.example>out.txt",
            "com.example`",
            "com.example$(whoami)",
            "1com.example", # starts with number
            ".com.example", # starts with dot
            "com.example.", # ends with dot
            "com..example", # consecutive dots
            "com.ex ample"  # contains space
        ]
        for name in invalid_names:
            self.assertFalse(ADBOperations.is_valid_package_name(name), f"Should be invalid: {name}")

    @patch('adb_operations.ADBOperations._run_command')
    def test_uninstall_package_invalid_name(self, mock_run_command):
        result = self.adb.uninstall_package("com.example; rm -rf /")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Invalid package name format")
        mock_run_command.assert_not_called()

    @patch('adb_operations.ADBOperations._run_command')
    def test_reinstall_package_invalid_name(self, mock_run_command):
        result = self.adb.reinstall_package("com.example; rm -rf /")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Invalid package name format")
        mock_run_command.assert_not_called()

if __name__ == '__main__':
    unittest.main()
