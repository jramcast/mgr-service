import os
import sys
import logging

from mgr.infrastructure.server.flask import Server
from mgr.usecases.classify import ClassifyUseCase
from mgr.infrastructure.models.naive_bayes.naivebayes import NaiveBayesModel
from mgr.infrastructure.models.deep.feed_forward import FeedForwardNetworkModel
from mgr.infrastructure.models.deep.lstm import LSTMRecurrentNeuralNetwork
from mgr.infrastructure.models.svm.svm import SVMModel
from mgr.infrastructure.youtube import (
    YoutubeAudioLoader, VideoInfoCacheInMemory)
from mgr.infrastructure.audioset.vggish.cache.memory import (
    InMemoryFeaturesCache
)
from mgr.infrastructure.audioset.vggish.loader import EmbeddingsLoader
from flask import request

# Tensorflow serving urls
# Models in TF are served separately with TF Serving
VGGISH_PREDICT_URL = os.environ.get(
    "VGGISH_PREDICT_URL",
    "http://vggish:8501/v1/models/vggish:predict")
FFN_PREDICT_URL = os.environ.get(
    "FFN_PREDICT_URL",
    "http://ff_network:8501/v1/models/ff_network:predict")
RNN_PREDICT_URL = os.environ.get(
    "RNN_PREDICT_URL",
    "http://lstm_network:8501/v1/models/lstm_network:predict")

PROXIES = [proxy.strip() for proxy in os.environ.get("PROXIES", "").split(",")]
PROXIES = [proxy for proxy in PROXIES if proxy]


logger = logging.getLogger("mgr-service")
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
logger.addHandler(out_hdlr)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


features_cache = InMemoryFeaturesCache()
embeddings_loader = EmbeddingsLoader(VGGISH_PREDICT_URL, features_cache)

# Models to classify
models = [
    NaiveBayesModel(embeddings_loader),
    FeedForwardNetworkModel(FFN_PREDICT_URL, embeddings_loader),
    LSTMRecurrentNeuralNetwork(RNN_PREDICT_URL, embeddings_loader),
    SVMModel(embeddings_loader)
]

# Audio downloader
youtube_cache = VideoInfoCacheInMemory()
audio_downloader = YoutubeAudioLoader(youtube_cache, logger, PROXIES)


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
