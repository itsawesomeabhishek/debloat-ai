import unittest
from adb_operations import ADBOperations

class TestADBOperations(unittest.TestCase):
    def setUp(self):
        self.adb = ADBOperations()

    def test_guess_package_type_system(self):
        system_packages = [
            "com.android.systemui",
            "com.google.android.gms",
            "com.samsung.android.app",
            "com.xiaomi.finddevice",
            "com.huawei.system",
            "com.oppo.camera",
            "com.vivo.browser"
        ]
        for pkg in system_packages:
            with self.subTest(pkg=pkg):
                self.assertEqual(self.adb._guess_package_type(pkg), "system")

    def test_guess_package_type_user(self):
        user_packages = [
            "com.facebook.katana",
            "org.videolan.vlc",
            "com.example.app",
            "net.domain.app"
        ]
        for pkg in user_packages:
            with self.subTest(pkg=pkg):
                self.assertEqual(self.adb._guess_package_type(pkg), "user")

    def test_guess_package_type_edge_cases(self):
        # Exact prefix match but missing the trailing dot should be classified as user
        # unless it happens to match another condition.
        # e.g. "com.android" does not start with "com.android."
        edge_cases_user = [
            "com.android",
            "com.google",
            "com.samsung",
            "com.xiaomi",
            "com.huawei",
            "com.oppo",
            "com.vivo"
        ]
        for pkg in edge_cases_user:
            with self.subTest(pkg=pkg):
                self.assertEqual(self.adb._guess_package_type(pkg), "user")

if __name__ == '__main__':
    unittest.main()
