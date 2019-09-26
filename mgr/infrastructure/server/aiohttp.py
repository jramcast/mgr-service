from aiohttp import web

from service.redirection.requests import (
    MetasRedirectRequest,
    MetaPosByHotelRequest
)
from service.redirection.interfaces import UseCaseInterface
from service.routes import Routes


class Server:

    predict_controller: PredictController

    def __init__(
        self,
        predict_controller: PredictController,
    ):
        self.predict_controller = predict_controller
        self.app = web.Application()
        self.app.add_routes([
            web.get("/", self.home),
            web.get("/recognize", self.recognize),
        ])

    def serve(self, port=3000):
        web.run_app(self.app, port=port)

    async def home(self, request):
        text = "Welcome to the awesome Music Recognition Service!"
        return web.Response(text=text)

    async def recognize(self, request):
        self.predict_controller.recognize()
