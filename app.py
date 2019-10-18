from mgr.infrastructure.server.flask import Server
from mgr.usecases.classify import ClassifyUseCase
from mgr.infrastructure.models.naivebayes import NaiveBayesModel
from mgr.infrastructure.youtube import YoutubeAudioLoader
from flask import request


# List of models to classify
models = [
    NaiveBayesModel()
]

# Audio downloader
audio_downloader = YoutubeAudioLoader()


# Use case initialization
classify = ClassifyUseCase(models, audio_downloader)


# Server and routes defintion
server = Server()


@server.route("/classify")
def route_classify():
    return classify.run(request.args["clip"])


# Flask needs to read the app variable to start
app = server.serve()
