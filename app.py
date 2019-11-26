from mgr.infrastructure.server.flask import Server
from mgr.usecases.classify import ClassifyUseCase
from mgr.infrastructure.models.naive_bayes.naivebayes import NaiveBayesModel
from mgr.infrastructure.models.deep.feed_forward import FeedForwardNetworkModel
from mgr.infrastructure.models.deep.lstm import LSTMRecurrentNeuralNetwork
from mgr.infrastructure.models.svm.svm import SVMModel
from mgr.infrastructure.youtube import YoutubeAudioLoader
from mgr.infrastructure.audioset.vggish.cache.memory import (
    InMemoryFeaturesCache
)
from mgr.infrastructure.audioset.vggish.loader import EmbeddingsLoader
from flask import request





features_cache = InMemoryFeaturesCache()
embeddings_loader = EmbeddingsLoader(
    "http://vggish:8501/v1/models/vggish:predict",
    features_cache
)

# Models to classify
models = [
    NaiveBayesModel(embeddings_loader),
    FeedForwardNetworkModel(
        "http://ff_network:8501/v1/models/ff_network:predict",
        embeddings_loader),
    LSTMRecurrentNeuralNetwork(
        "http://lstm_network:8501/v1/models/lstm_network:predict",
        embeddings_loader),
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
