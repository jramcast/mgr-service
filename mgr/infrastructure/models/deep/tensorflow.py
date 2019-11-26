import json
from typing import List

import requests
import numpy as np

from mgr.usecases.interfaces import Model, AudioSegment, Prediction
from mgr.infrastructure.audioset.vggish.loader import EmbeddingsLoader
from mgr.infrastructure.audioset.ontology import MUSIC_GENRE_CLASSES


class TensorFlowServingModelClient(Model):
    """
    Client class to consume models deployed with Tensorflow Serving
    """

    def __init__(
        self,
        model_service_url: str,
        embeddings_loader: EmbeddingsLoader
    ):
        self.model_service_url = model_service_url
        self.embeddings_loader = embeddings_loader

    def preprocess(self, segments: List[AudioSegment]):
        # At this point, both the full clip and its segments
        # are supossed to be downloaded
        embeddings = self.embeddings_loader.load_from_segments(segments)
        x = np.array(embeddings)
        return x

    def classify(
        self, embeddings: np.ndarray
    ) -> List[List[Prediction]]:
        """
        Returns a list of list of predictions
        The first list is the list of samples(segments)
        The second list is the list of labels for each segment
        """
        payload = json.dumps({"instances": embeddings.tolist()})
        print("model payload", payload)
        r = requests.post(
            self.model_service_url,
            data=payload,
            headers={"content-type": "application/json"}
        )
        result = json.loads(r.text)['predictions']
        print("\n --> result", result)

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