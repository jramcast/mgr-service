from abc import ABC
from ..domain import entities




class Model(ABC):

    def predict(self, features: entities.ModelInputFeatures):
        raise NotImplementedError()