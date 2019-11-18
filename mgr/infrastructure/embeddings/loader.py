from typing import List

from . import extractor
from ...domain.entities import AudioSegment
from ...usecases.interfaces import FeaturesCache


class EmbeddingsLoader:

    """
    Loads extracted embeddings from a list of audio segments
    """

    def __init__(self, cache: FeaturesCache):
        self.cache = cache

    def load_from_segments(self, segments: List[AudioSegment]) -> List:
        features = []

        for segment in segments:
            if segment.filename in self.cache:
                print(segment.filename, "getting from cache!")
                segment_features = self.cache.get(segment.filename)
            else:
                segment_features = extractor.extract(segment.filename)
                self.cache.set(segment.filename, segment_features)

            features.append(segment_features)

        return features
