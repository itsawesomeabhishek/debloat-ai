import unittest
from unittest.mock import MagicMock, patch
from adb_operations import ADBOperations
from ai_advisor import AIAdvisor

class TestADBSecurity(unittest.TestCase):

    def test_is_valid_package_name(self):
        """Test the package name validation logic"""
        # Valid package names
        self.assertTrue(ADBOperations.is_valid_package_name("com.example.app"))
        self.assertTrue(ADBOperations.is_valid_package_name("android"))
        self.assertTrue(ADBOperations.is_valid_package_name("com.samsung.android.app.contacts"))
        self.assertTrue(ADBOperations.is_valid_package_name("a.b.c"))
        self.assertTrue(ADBOperations.is_valid_package_name("com.facebook.katana"))
        self.assertTrue(ADBOperations.is_valid_package_name("package_name123"))

        # Invalid package names (injections/malformed)
        self.assertFalse(ADBOperations.is_valid_package_name("com.example.app; rm -rf /"))
        self.assertFalse(ADBOperations.is_valid_package_name("com.example.app && ls"))
        self.assertFalse(ADBOperations.is_valid_package_name("--user 0"))
        self.assertFalse(ADBOperations.is_valid_package_name("-rf"))
        self.assertFalse(ADBOperations.is_valid_package_name("com.app--flag"))
        self.assertFalse(ADBOperations.is_valid_package_name("com..example"))
        self.assertFalse(ADBOperations.is_valid_package_name(".com.example"))
        self.assertFalse(ADBOperations.is_valid_package_name("com.example."))
        self.assertFalse(ADBOperations.is_valid_package_name("1com.example"))
        self.assertFalse(ADBOperations.is_valid_package_name("com.example "))
        self.assertFalse(ADBOperations.is_valid_package_name(""))
        self.assertFalse(ADBOperations.is_valid_package_name(None))

    def test_uninstall_package_injection(self):
        """Test that uninstall_package rejects invalid package names without running commands"""
        adb = ADBOperations()
        adb._run_command = MagicMock()

        result = adb.uninstall_package("com.example.app; rm -rf /")

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Invalid package name")
        adb._run_command.assert_not_called()

    def test_reinstall_package_injection(self):
        """Test that reinstall_package rejects invalid package names without running commands"""
        adb = ADBOperations()
        adb._run_command = MagicMock()

        result = adb.reinstall_package("--user 0 com.example.app")

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Invalid package name")
        adb._run_command.assert_not_called()

    def test_ai_advisor_injection(self):
        """Test that AIAdvisor rejects invalid package names without making API calls"""
        advisor = AIAdvisor(provider="perplexity")

        # Test with invalid package name
        result = advisor.analyze_package("com.example.app && echo 'hacked'")

        self.assertIn("error", result)
        self.assertEqual(result["error"], "Invalid package name")
        self.assertEqual(result["safetyLevel"], "unknown")

        # We don't need to mock requests if we just assert it returns the error dict immediately.

if __name__ == '__main__':
    unittest.main()
