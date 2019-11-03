import joblib
import numpy as np
from typing import List
from dataclasses import dataclass
from ...usecases.interfaces import Model
from ...domain.entities import Prediction, AudioSegment
from .. import embeddings
from ..ontology import MUSIC_GENRE_CLASSES


@dataclass
class NaiveBayesInputFeatures():
    pass


class NaiveBayesModel(Model):

    def __init__(self):
        model_file = "./mgr/infrastructure/models/bal_bayes.joblib"
        self.model = joblib.load(model_file)

    def preprocess(self, segments: List[AudioSegment]):
        # At this point, both the full clip and its segments are supossed to be downloaded
        x = np.array(
            [embeddings.extract(segment.filename) for segment in segments]
        )
        x = x.reshape(x.shape[0], 1280)
        print("x shape", x.shape)
        return x
        # return x.reshape(-1, 1280)

    def classify(
        self, features: NaiveBayesInputFeatures
    ) -> List[List[Prediction]]:
        """
        Returns a list of list of predictions
        The first list is the list of samples(segments)
        The second list is the list of labels for each segment
        """
        result = self.model.predict_proba(features)

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
