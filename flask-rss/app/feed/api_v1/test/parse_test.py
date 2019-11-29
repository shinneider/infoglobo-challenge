import json
import unittest
from app.feed.api_v1.test import mocks
from app.feed.api_v1.parse import parse_feed_json, parse_summary_json
from main import app


class TestParseFeedJson(unittest.TestCase):

    def setUp(self):
        client = app.test_client()
        self.response = client.get('/')

    def test_feed_summary(self):
        summary = parse_summary_json(mocks.feed_sumary_raw_data)

        if not json.dumps(summary) == json.dumps(mocks.feed_summary_response):
            self.fail('Summary response is not equal to expected response')

    def test_feed(self):
        status, response = parse_feed_json(mocks.feed_raw_data)
        self.assertEqual(status, True)
        if json.dumps(response) == json.dumps(mocks.feed_response):
            self.fail('Feed Json response is not equal to expected response')

    def test_invalid_summary_tag(self):
        summary = """<div><tr><td></td></tr></div>"""
        self.assertEqual(parse_summary_json(summary), [])

    def test_invalid_feed_entries(self):
        status, response = parse_feed_json("""<div></div>""")
        self.assertEqual(status, False)
        self.assertEqual(response, [])

    def test_invalid_feed_entries_struct(self):
        status, response = parse_feed_json("""<item></item>""")
        self.assertEqual(status, False)
        self.assertEqual(response, [])