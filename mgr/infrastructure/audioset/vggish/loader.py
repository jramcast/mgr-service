import json
from typing import List

import requests
import numpy as np

from mgr.domain.entities import AudioSegment
from mgr.usecases.interfaces import FeaturesCache
from .model.vggish_postprocess import Postprocessor
from .model.vggish_input import wavfile_to_examples


class EmbeddingsLoader:

    """
    Loads extracted embeddings from a list of audio segments
    """

    def __init__(
        self,
        model_service_url: str,
        cache: FeaturesCache
    ):
        self.model_service_url = model_service_url
        self.cache = cache
        self.pproc = Postprocessor(
            "data/vggish/vggish_pca_params.npz"
        )

    def load_from_segments(self, segments: List[AudioSegment]) -> List:
        features = []

        for segment in segments:
            if segment.filename in self.cache:
                segment_features = self.cache.get(segment.filename)
                print("Embeddings extracted from cache (HIT)")
            else:
                segment_features = self.extract_embeddings(segment.filename)
                self.cache.set(segment.filename, segment_features)
                print("Embeddings extracted from VGGISH (MISS)")

            features.append(segment_features)

        return features

    def extract_embeddings(self, filename):
        example_batch = wavfile_to_examples(filename)
        payload = json.dumps({"instances": example_batch.tolist()})
        r = requests.post(
            self.model_service_url,
            data=payload,
            headers={"content-type": "application/json"}
        )

        result = json.loads(r.text)['predictions']

        postprocessed_batch = self.pproc.postprocess(np.array(result))

        return np.array(postprocessed_batch)
