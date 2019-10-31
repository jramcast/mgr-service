from typing import List, Any, Dict
from .interfaces import Model, AudioLoader
from ..domain.entities import Prediction


class ClassifyUseCase:

    models: List[Model]

    def __init__(self, models: Dict[str, Model], audio_loader: AudioLoader):
        self.models = models
        self.audio_loader = audio_loader

    def run(self, uri, model_id) -> List[Any]:
        clip = self.audio_loader.load(uri)
        results = {}

        model = self.models[model_id]
        samples = model.preprocess(clip.segments)
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


class ClassifySegmentUseCase:

    models: List[Model]

    def __init__(self, models: List[Model], audio_loader: AudioLoader):
        self.models = models
        self.audio_loader = audio_loader

    def run(self, uri, segment_index: int) -> List[Any]:
        clip = self.audio_loader.load(uri)
        results = {}

        if segment_index >= len(clip.segments):
            return {
                "results": {},
                "segment": segment_index,
                "nextSegment": None
            }

        segment = clip.segments[segment_index]

        for model in self.models:
            samples = model.preprocess([segment])
            predictions = model.classify(samples)
            results[model.name] = self.to_dict(predictions)

        if segment_index < len(clip.segments) - 1:
            next_segment_index = segment_index + 1
        else:
            next_segment_index = None

        return {
            "results": results,
            "segment": segment_index,
            "nextSegment": next_segment_index
        }

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


class ClassifySegmentFromSecondUseCase:

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
            results[model.name] = self.to_dict(predictions)

        return {
            "results": results,
            "segment": segment
        }

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
