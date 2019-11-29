from app.feed.api_v1.views import GetRSSData
from flask_restful import Resource, Api

urlpatterns = [
    ('json', GetRSSData, {'endpoint': 'rss'}),
]
