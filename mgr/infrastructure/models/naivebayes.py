from dataclasses import dataclass
from ...usecases.interfaces import Model
from ...domain.entities import AudioClip


@dataclass
class NaiveBayesInputFeatures():
    pass


class NaiveBayesModel(Model):

    def preprocess(self, clip: AudioClip):
        pass

    def classify(self, features: NaiveBayesInputFeatures):
        return "Flamenco"
