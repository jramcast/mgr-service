import abc
from typing import List, Any


class Model(abc.ABC):

    @abc.abstractmethod
    def predict(self):
        raise NotImplementedError()


class PredictUseCase:

    models: List[Model]

    def __init__(self, models: List[Model]):
        self.models = models

    def run(self) -> List[Any]:
        return [model.predict for model in self.models]
