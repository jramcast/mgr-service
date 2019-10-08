
from typing import List, Any
from .interfaces import Model
from ..domain.entities import ClassificationResult


class ClassifyUseCase:

    models: List[Model]

    def __init__(self, models: List[Model]):
        self.models = models

    def run(self, data) -> List[Any]:
        results = [model.classify(data) for model in self.models]
        return [self.to_dict(result) for result in results]

    def to_dict(self, result: ClassificationResult):
        return [{
            "label": label.name,
            "score": label.score
        } for label in result.labels]
