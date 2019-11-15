from mgr.infrastructure.server.flask import Server
from mgr.usecases.classify import ClassifyUseCase
from mgr.infrastructure.models.naivebayes import NaiveBayesModel
from mgr.infrastructure.models.neuralnetwork import NeuralNetworkModel
from mgr.infrastructure.models.lstm import LSTMRecurrentNeuralNetwork
from mgr.infrastructure.models.svm import SVMModel
from mgr.infrastructure.youtube import YoutubeAudioLoader
from mgr.infrastructure.embeddings.cache.memory import InMemoryFeaturesCache
from mgr.infrastructure.embeddings.loader import EmbeddingsLoader
from flask import request


features_cache = InMemoryFeaturesCache()
embeddings_loader = EmbeddingsLoader(features_cache)

# Models to classify
models = [
    NaiveBayesModel(embeddings_loader),
    NeuralNetworkModel(embeddings_loader),
    LSTMRecurrentNeuralNetwork(embeddings_loader),
    SVMModel(embeddings_loader)
]

# Audio downloader
audio_downloader = YoutubeAudioLoader()


# Use case initialization
classify = ClassifyUseCase(models, audio_downloader)


# Server and routes defintion
server = Server()


@server.route("/segment/classify")
def route_segment_classify():
    return classify.run(
        request.args["clip"],
        round(float(request.args["from"]))
    )


# Flask needs to read the app variable to start
app = server.serve()
