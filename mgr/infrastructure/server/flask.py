from flask import Flask
from flask_cors import CORS


class Server:

    __slots__ = ["app", "route"]

    def __init__(self):

        self.app = Flask(__name__, static_folder='/home/jaime/Desarrollo/phd/mgr-service/static',)
        CORS(self.app)
        self.route = self.app.route

        @self.app.route('/')
        def hello_world():
            return {
                "info": "Service to predict music genre out of music clips",
                "urls": ['%s' % rule for rule in self.app.url_map.iter_rules()]
            }

    def serve(self):
        return self.app
