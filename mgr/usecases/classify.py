from typing import List, Any
from .interfaces import Model, AudioLoader
from ..domain.entities import Prediction


class ClassifyUseCase:

    models: List[Model]

    def __init__(self, models: List[Model], audio_loader: AudioLoader):
        self.models = models
        self.audio_loader = audio_loader

    def run(self, uri) -> List[Any]:
        clip = self.audio_loader.load(uri)
        results = {}

        for model in self.models:
            samples = model.preprocess(clip)
            predictions = model.classify(samples)
            results[model.name] = self.to_dict(predictions)

        return results

    def to_dict(self, predictions: List[List[Prediction]]):
        formatted_segments = []
        for segment in predictions:
            formatted_segment = []
            formatted_segments.append(formatted_segment)
            for prediction in segment:
                formatted_segment.append({
                    "label": prediction.label,
                    "score": prediction.score
                })

        return formatted_segments
