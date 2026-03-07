import unittest
from openclaw_integration import ActionExecutor

class TestBloatwareDetector(unittest.TestCase):
    def setUp(self):
        # ActionExecutor needs an ADBOperations instance, but we can pass None
        # since _is_likely_bloatware doesn't use it.
        self.executor = ActionExecutor(None)

    def test_standard_bloatware(self):
        self.assertTrue(self.executor._is_likely_bloatware("com.facebook.katana"))
        self.assertTrue(self.executor._is_likely_bloatware("com.samsung.android.messaging"))
        self.assertTrue(self.executor._is_likely_bloatware("com.amazon.mShop.android.shopping"))
        self.assertTrue(self.executor._is_likely_bloatware("com.ss.android.ugc.trill")) # TikTok

    def test_non_bloatware_user_apps(self):
        self.assertFalse(self.executor._is_likely_bloatware("com.whatsapp"))
        self.assertFalse(self.executor._is_likely_bloatware("org.mozilla.firefox"))
        self.assertFalse(self.executor._is_likely_bloatware("com.google.android.apps.maps"))

    def test_critical_system_apps(self):
        self.assertFalse(self.executor._is_likely_bloatware("com.android.systemui"))
        self.assertFalse(self.executor._is_likely_bloatware("com.google.android.gms"))
        self.assertFalse(self.executor._is_likely_bloatware("com.android.phone"))
        self.assertFalse(self.executor._is_likely_bloatware("com.android.settings"))

    def test_case_insensitivity(self):
        self.assertTrue(self.executor._is_likely_bloatware("COM.FACEBOOK.ORCA"))
        self.assertTrue(self.executor._is_likely_bloatware("TikTok"))

    def test_substrings(self):
        self.assertTrue(self.executor._is_likely_bloatware("my.game.app"))
        self.assertTrue(self.executor._is_likely_bloatware("weather.provider"))
        self.assertTrue(self.executor._is_likely_bloatware("prefix.netflix.suffix"))

    def test_edge_cases(self):
        self.assertFalse(self.executor._is_likely_bloatware(""))
        self.assertFalse(self.executor._is_likely_bloatware("a" * 1000))
        self.assertTrue(self.executor._is_likely_bloatware("facebook")) # Exactly an indicator

if __name__ == '__main__':
    unittest.main()
