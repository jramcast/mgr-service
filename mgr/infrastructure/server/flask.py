from flask import Flask
from ...usecases.predict import PredictUseCase


class Server:

    predict_usecase: PredictUseCase

    def __init__(
        self,
        predict_usecase: PredictUseCase,
    ):
        self.predict_usecase = predict_usecase
        self.app = Flask(__name__)

        @self.app.route('/')
        def hello_world():
            return self.predict_usecase.run()

    def serve(self):
        return self.app
