import unittest
from unittest.mock import patch, MagicMock
import json
import requests
import os

from ai_advisor import AIAdvisor


class TestAIAdvisor(unittest.TestCase):
    def setUp(self):
        # Set a mock API key so that self.api_key is not None
        os.environ['PERPLEXITY_API_KEY'] = 'mock_api_key'
        self.advisor = AIAdvisor(provider="perplexity")

    @patch('requests.post')
    def test_analyze_package_request_exception(self, mock_post):
        # Mock requests.post to raise a RequestException
        mock_post.side_effect = requests.exceptions.RequestException("Network timeout")

        with self.assertRaisesRegex(Exception, r"API request failed: Network timeout"):
            self.advisor.analyze_package("com.example.app")

    @patch('requests.post')
    def test_analyze_package_json_decode_error(self, mock_post):
        # Mock requests.post to return a valid response but with invalid JSON in the content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Invalid JSON content right here"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        with self.assertRaisesRegex(Exception, r"Failed to parse AI response:.*"):
            self.advisor.analyze_package("com.example.app")

    @patch('requests.post')
    def test_analyze_package_generic_exception(self, mock_post):
        # Mock requests.post to raise a generic Exception
        mock_post.side_effect = Exception("Some weird error")

        with self.assertRaisesRegex(Exception, r"Analysis failed: Some weird error"):
            self.advisor.analyze_package("com.example.app")

if __name__ == '__main__':
    unittest.main()
