
from typing import List, Any
from .interfaces import Model
from ..domain.entities import ClassificationResult


class ClassifyUseCase:

    models: List[Model]

    def __init__(self, models: List[Model], audio_loader):
        self.models = models
        # TODO: self.audio_loader = audio_loader
        # TODO: self.preprocessor = preprocessor

    def run(self, data) -> List[Any]:
        # TODO: audio = self.audio_loader(audioid).load()

        # TODO: segment = audio.get_first_segment()

        # TODO: embeddings = self.preprocessor.preprocess(segment)

        results = [model.classify(data) for model in self.models]
        return [self.to_dict(result) for result in results]

    def to_dict(self, result: ClassificationResult):
        return [{
            "label": label.name,
            "score": label.score
        } for label in result.labels]
