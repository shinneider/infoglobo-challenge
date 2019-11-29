import requests
import unittest
from unittest.mock import patch
from app.feed.api_v1.crawler import get_site_data


class TestCrawlerGetData(unittest.TestCase):

    @patch('requests.get')
    def test_valid_status_code(self, mock_request):
        for status in [200, 201, 400, 401, 403, 404, 405, 500]:
            mock_request.return_value.status_code = status
            mock_request.return_value.text = 'test'
            status, response = get_site_data(url='invalid.url', 
                                             expected_status=status)
            self.assertEqual(status, True)
            self.assertEqual(response, 'test')

    @patch('requests.get')
    def test_valid_site_text_response(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.text = '{"user": "test"}'
        status, response = get_site_data(url='www.test.invalid')
        self.assertEqual(status, True)
        self.assertEqual(response, '{"user": "test"}')

    @patch('requests.get')
    def test_valid_site_json_response(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json = {"user": "test"}
        status, response = get_site_data(url='www.test.invalid', output='json')
        self.assertEqual(status, True)
        self.assertEqual(response, {"user": "test"})

    @patch('requests.get')
    def test_invalid_status_code(self, mock_request):
        mock_request.return_value.status_code = 500
        mock_request.return_value.text = 'test'
        status, response = get_site_data(url='invalid.url', 
                                         expected_status=200)
        self.assertEqual(status, False)
        self.assertEqual(response, 'test')

    @patch('requests.get')
    def test_invalid_request_exception(self, mock_request):
        mock_request.side_effect = requests.exceptions.ConnectionError(
                                                'testing erro conection')
        status, response = get_site_data(url='www.test.invalid')
        self.assertEqual(status, False)
        self.assertEqual(response, None)

    def test_invalid_output_argument(self):
        with self.assertRaises(ValueError) as context:
            get_site_data(url='invalid.url', output='xml')

        self.assertEqual('Output expect `text` or `json` values', str(
                                                        context.exception))