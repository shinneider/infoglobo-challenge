from app.shared.flask_utils.restfull_url import include

urlpatterns = [
    ('/v1/rss/', include('app.feed.api_v1.urls')),
]