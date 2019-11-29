from app.shared.flask_utils.restfull_url import include as urls_import
from config import settings

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

urls = urls_import(settings.ROOT_URLCONF)
for url in urls:
    params = url[2] if len(url) > 2 else {}
    api.add_resource(url[1], url[0], **params)

if __name__ == '__main__':
    app.run(
        debug=settings.DEBUG,
        host='0.0.0.0',
        port=8000
    )