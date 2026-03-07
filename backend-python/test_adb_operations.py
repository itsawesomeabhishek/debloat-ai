import unittest
from adb_operations import ADBOperations

class TestADBOperationsSafetyLevel(unittest.TestCase):
    def setUp(self):
        self.adb = ADBOperations()

    def test_dangerous_level(self):
        # Exact matches in dangerous_packages
        self.assertEqual(self.adb._determine_safety_level('com.android.systemui'), 'Dangerous')
        self.assertEqual(self.adb._determine_safety_level('com.android.phone'), 'Dangerous')
        self.assertEqual(self.adb._determine_safety_level('com.android.settings'), 'Dangerous')
        self.assertEqual(self.adb._determine_safety_level('com.android.launcher'), 'Dangerous')
        self.assertEqual(self.adb._determine_safety_level('com.android.launcher3'), 'Dangerous')
        self.assertEqual(self.adb._determine_safety_level('com.android.vending'), 'Dangerous')

    def test_expert_level(self):
        # Prefixes in expert_prefixes
        self.assertEqual(self.adb._determine_safety_level('com.google.android.gms'), 'Expert')
        self.assertEqual(self.adb._determine_safety_level('com.google.android.gms.test'), 'Expert')
        self.assertEqual(self.adb._determine_safety_level('com.google.android.gsf'), 'Expert')
        self.assertEqual(self.adb._determine_safety_level('com.android.bluetooth'), 'Expert')
        self.assertEqual(self.adb._determine_safety_level('com.android.nfc'), 'Expert')

    def test_caution_level(self):
        # Prefixes in caution_prefixes
        self.assertEqual(self.adb._determine_safety_level('com.samsung.android.app'), 'Caution')
        self.assertEqual(self.adb._determine_safety_level('com.xiaomi.finddevice'), 'Caution')
        self.assertEqual(self.adb._determine_safety_level('com.miui.securitycenter'), 'Caution')
        self.assertEqual(self.adb._determine_safety_level('com.huawei.systemmanager'), 'Caution')
        self.assertEqual(self.adb._determine_safety_level('com.oppo.camera'), 'Caution')
        self.assertEqual(self.adb._determine_safety_level('com.vivo.gallery'), 'Caution')
        self.assertEqual(self.adb._determine_safety_level('com.realme.movies'), 'Caution')
        self.assertEqual(self.adb._determine_safety_level('com.oneplus.notes'), 'Caution')

    def test_safe_level(self):
        # Default cases (not matching any of the above)
        self.assertEqual(self.adb._determine_safety_level('com.facebook.katana'), 'Safe')
        self.assertEqual(self.adb._determine_safety_level('com.whatsapp'), 'Safe')
        self.assertEqual(self.adb._determine_safety_level('com.instagram.android'), 'Safe')

    def test_edge_cases(self):
        # Empty string
        self.assertEqual(self.adb._determine_safety_level(''), 'Safe')

        # Case sensitivity (dangerous_packages are lowercase, exact match)
        self.assertEqual(self.adb._determine_safety_level('Com.Android.SystemUI'), 'Safe')

        # Substring but not prefix (should be Safe)
        self.assertEqual(self.adb._determine_safety_level('com.fake.com.android.systemui'), 'Safe')
        self.assertEqual(self.adb._determine_safety_level('my.com.samsung.app'), 'Safe')

        # Prefix but not an exact match for dangerous (should be Safe)
        self.assertEqual(self.adb._determine_safety_level('com.android.systemui.overlay'), 'Safe')

        # None type should raise AttributeError due to startswith/in on string
        with self.assertRaises(AttributeError):
            self.adb._determine_safety_level(None)

if __name__ == '__main__':
    unittest.main()
