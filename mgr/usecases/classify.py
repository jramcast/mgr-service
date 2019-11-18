from typing import List, Any, Dict
from .interfaces import Model, AudioLoader
from ..domain.entities import Prediction



class ClassifyUseCase:

    models: List[Model]

    def __init__(self, models: List[Model], audio_loader: AudioLoader):
        self.models = models
        self.audio_loader = audio_loader

    def run(self, uri, from_second: int) -> List[Any]:
        segment = self.audio_loader.load_segment(uri, from_second)
        results = {}

        for model in self.models:
            samples = model.preprocess([segment])
            predictions = model.classify(samples)
            results[model.name] = self.to_dict(predictions, uri, from_second)

        return results

    def to_dict(self, predictions: List[List[Prediction]], uri, from_second):
        segment = predictions[0]
        formatted_segment = {
            "labels": [],
            "segment": {
                "mediaUri": uri,
                "fromSecond": from_second,
                "toSecond": from_second + 10
            }
        }

        for prediction in segment:
            formatted_segment["labels"].append({
                "name": prediction.label,
                "score": float(prediction.score)
            })

        return formatted_segment
