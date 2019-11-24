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

    def load_from_segments(self, segments: List[AudioSegment]) -> List:
        features = []

        for segment in segments:
            if segment.filename in self.cache:
                print(segment.filename, "getting from cache!")
                segment_features = self.cache.get(segment.filename)
            else:
                segment_features = self.extract_embeddings(segment.filename)
                self.cache.set(segment.filename, segment_features)

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

        # TODO: move this to constructor
        pproc = Postprocessor(
            "data/vggish/vggish_pca_params.npz"
        )
        postprocessed_batch = pproc.postprocess(np.array(result))
        return np.array(postprocessed_batch)
