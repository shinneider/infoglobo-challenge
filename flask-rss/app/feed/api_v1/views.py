from flask_restful import Resource
from app.feed.api_v1.crawler import get_site_data
from app.feed.api_v1.parse import parse_feed_json
from app.shared.logger import Logger
from app.shared.permissions import Auth, IsAuthenticated
from config import settings


@Auth
class GetRSSData(Resource):
    """
    """
    permission_classes = IsAuthenticated

    def get(self):
        """
            Process and parse RSS data to a json
        """
        status, data = get_site_data(url=settings.RSS_URL)
        if not status:
            return ({'error': "Unable to contact a source"}, 500)

        try:
            status, data = parse_feed_json(data)
            if not status:
                raise Exception()

            return ({'feed': data}, 200)
        except Exception as err:
            Logger.error(f'erro in feed parse: {err}')
            return ({'error': "There was an error in processing your request"}, 500)