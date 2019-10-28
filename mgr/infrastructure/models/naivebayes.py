import joblib
import numpy as np
from typing import List
from dataclasses import dataclass
from ...usecases.interfaces import Model
from ...domain.entities import AudioClip, Prediction
from .. import embeddings
from ..ontology import MUSIC_GENRE_CLASSES


@dataclass
class NaiveBayesInputFeatures():
    pass


class NaiveBayesModel(Model):

    def __init__(self):
        model_file = "./mgr/infrastructure/models/bal_bayes.joblib"
        self.model = joblib.load(model_file)

    def preprocess(self, clip: AudioClip):
        # At this point, both the full clip and its segments are supossed to be downloaded
        x = np.array(
            [embeddings.extract(segment.filename) for segment in clip.segments]
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
        result = self.model.predict(features)
        result_probs = self.model.predict_proba(features)

        print("SHAPE", result.shape)

        predictions = []
        for i, record in enumerate(result):
            segment_predictions = []
            predictions.append(segment_predictions)
            for j, prediction in enumerate(record):
                if prediction == 1:
                    segment_predictions.append(Prediction(
                        MUSIC_GENRE_CLASSES[j]["name"],
                        result_probs[i][j]
                    ))

        return predictions
