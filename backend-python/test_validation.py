import unittest
from adb_operations import ADBOperations

class TestPackageNameValidation(unittest.TestCase):
    def test_valid_package_names(self):
        valid_names = [
            "com.example.app",
            "com.android.systemui",
            "android",
            "com.samsung.android.messaging",
            "com.example_123.app",
            "a.b.c"
        ]
        for name in valid_names:
            self.assertTrue(ADBOperations.is_valid_package_name(name), f"Expected '{name}' to be valid")

    def test_invalid_package_names(self):
        invalid_names = [
            "com.example.app; rm -rf /",
            "com.example..app",
            ".com.example.app",
            "com.example.app.",
            "com.-example.app",
            "com.example.app$",
            "com.example.app|",
            "com.example.app > /dev/null",
            "",
            "1com.example.app",
            "com.1example.app"
        ]
        for name in invalid_names:
            self.assertFalse(ADBOperations.is_valid_package_name(name), f"Expected '{name}' to be invalid")

if __name__ == '__main__':
    unittest.main()
