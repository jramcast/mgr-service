from flask import Flask
from ...usecases.predict import ClassifyUseCase


class Server:

    predict_usecase: ClassifyUseCase

    def __init__(
        self,
        predict_usecase: ClassifyUseCase,
    ):
        self.predict_usecase = predict_usecase
        self.app = Flask(__name__)

        @self.app.route('/')
        def hello_world():
            return self.predict_usecase.run()

    def serve(self):
        return self.app
