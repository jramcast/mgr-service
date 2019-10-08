from aiohttp import web
from ...usecases.classify import ClassifyUseCase


class Server:

    classify_usecase: ClassifyUseCase

    def __init__(
        self,
        classify_usecase: ClassifyUseCase,
    ):
        self.classify_usecase = classify_usecase
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
        self.classify_usecase.recognize()
