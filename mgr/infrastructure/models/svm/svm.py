import joblib
import numpy as np
from typing import List
from ...usecases.interfaces import Model
from ...domain.entities import Prediction, AudioSegment
from ..ontology import MUSIC_GENRE_CLASSES
from ..embeddings.loader import EmbeddingsLoader


class SVMModel(Model):

    def __init__(self, embeddings_loader: EmbeddingsLoader):
        model_file = "./mgr/infrastructure/models/bal_svm.joblib"
        self.model = joblib.load(model_file)
        self.embeddings_loader = embeddings_loader

    def preprocess(self, segments: List[AudioSegment]):
        # At this point, both the full clip and its segments are supossed to be downloaded
        embeddings = self.embeddings_loader.load_from_segments(segments)
        x = np.array(embeddings)
        x = x.reshape(x.shape[0], 1280)
        print("x shape", x.shape)
        return x
        # return x.reshape(-1, 1280)

    def classify(
        self, features: np.ndarray
    ) -> List[List[Prediction]]:
        """
        Returns a list of list of predictions
        The first list is the list of samples(segments)
        The second list is the list of labels for each segment
        """
        result = self.model.decision_function(features)

        predictions = []
        for i, record in enumerate(result):
            segment_predictions = []
            predictions.append(segment_predictions)
            for j, prediction in enumerate(record):
                segment_predictions.append(Prediction(
                    MUSIC_GENRE_CLASSES[j]["name"],
                    result[i][j]
                ))

        return predictions
