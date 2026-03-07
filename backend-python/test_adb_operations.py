import unittest
from unittest.mock import patch
from adb_operations import ADBOperations, ADBError

class TestADBOperations(unittest.TestCase):
    @patch.object(ADBOperations, '_run_command')
    def test_get_device_info_no_device_connected(self, mock_run_command):
        """Test get_device_info raises ADBError when no device is connected"""
        # Mock the _run_command to return an empty string, simulating no devices
        mock_run_command.return_value = ""

        adb = ADBOperations()

        # Assert that ADBError is raised
        with self.assertRaises(ADBError) as context:
            adb.get_device_info()

        # Check that the exception message is correct
        self.assertEqual(str(context.exception), "No device connected")

        # Verify _run_command was called with correct arguments
        mock_run_command.assert_called_once_with([adb.adb_path, "devices", "-l"])

if __name__ == '__main__':
    unittest.main()
