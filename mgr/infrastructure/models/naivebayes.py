from dataclasses import dataclass
from ...domain.interfaces import Model


@dataclass
class NaiveBayesInputFeatures():
    pass


class NaiveBayesModel(Model):

    def predict(self, features: NaiveBayesInputFeatures):
        return "Flamenco"
