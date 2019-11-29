import unittest
from unittest.mock import patch
from main import app


class TestApiRss(unittest.TestCase):
    client = app.test_client()

    def test_unauthenticated_user(self):
        response = self.client.get('/v1/rss')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.decode('utf-8'), 
                         '{"error": "Authentication is required"}\n')

    @patch('app.feed.api_v1.views.parse_feed_json')
    def test_valid_data(self, mock_feed_json):
        mock_feed_json.return_value = (True, ['ok'])
        response = self.client.get('/v1/rss', headers={'auth': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), '{"feed": ["ok"]}\n')

    @patch('app.feed.api_v1.views.get_site_data')
    def test_get_site_data_erro(self, mock_site_data):
        mock_site_data.return_value = (False, None)
        response = self.client.get('/v1/rss', headers={'auth': 'true'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data.decode('utf-8'), 
                        '{"error": "Unable to contact a source"}\n')

    @patch('app.feed.api_v1.views.parse_feed_json')
    def test_parse_feed_json_erro(self, mock_feed_json):
        mock_feed_json.return_value = (False, None)
        response = self.client.get('/v1/rss', headers={'auth': 'true'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data.decode('utf-8'), 
                '{"error": "There was an error in processing your request"}\n')