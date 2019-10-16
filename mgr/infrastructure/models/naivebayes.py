import joblib
import numpy as np
from typing import List
from dataclasses import dataclass
from ...usecases.interfaces import Model
from ...domain.entities import AudioClip, ClassificationPrediction
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
        x = np.array(
            [embeddings.extract(segment.filename) for segment in clip.segments]
        )
        return x.reshape(-1, 1280)

    def classify(
        self, features: NaiveBayesInputFeatures
    ) -> List[ClassificationPrediction]:
        result = self.model.predict(features)
        result_probs = self.model.predict_proba(features)

        predictions = []
        for i, prediction in enumerate(result[0]):
            if prediction == 1:
                predictions.append({
                    "genre": MUSIC_GENRE_CLASSES[i]["name"],
                    "probability": result_probs[0][i]
                })
        return predictions
