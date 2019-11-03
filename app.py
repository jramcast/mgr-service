from mgr.infrastructure.server.flask import Server
from mgr.usecases.classify import (
    ClassifyUseCase, ClassifySegmentUseCase, ClassifySegmentFromSecondUseCase
)
from mgr.infrastructure.models.naivebayes import NaiveBayesModel
from mgr.infrastructure.models.neuralnetwork import NeuralNetworkModel
from mgr.infrastructure.models.lstm import LSTMRecurrentNeuralNetwork
from mgr.infrastructure.youtube import YoutubeAudioLoader
from flask import request


# Models to classify
models = {
    "naive_bayes": NaiveBayesModel(),
    "neural_network": NeuralNetworkModel(),
    "lstm": LSTMRecurrentNeuralNetwork()
}

# Audio downloader
audio_downloader = YoutubeAudioLoader()


# Use case initialization
classify = ClassifyUseCase(models, audio_downloader)
classify_segment = ClassifySegmentUseCase(models, audio_downloader)
classify_segment_fromseconds = ClassifySegmentFromSecondUseCase(models, audio_downloader)


# Server and routes defintion
server = Server()


@server.route("/classify")
def route_classify():
    return classify.run(request.args["clip"])


@server.route("/segment/classify")
def route_segment_classify():
    if "from" in request.args:
        return classify_segment_fromseconds.run(
            request.args["clip"],
            round(float(request.args["from"])),
            request.args["model"]
        )

    return classify_segment.run(
        request.args["clip"],
        int(request.args["segment"]),
        request.args["model"]
    )


# Flask needs to read the app variable to start
app = server.serve()
