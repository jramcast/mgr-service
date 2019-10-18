import abc
from typing import List
from ..domain.entities import AudioClip, Prediction


class Model(abc.ABC):

    @property
    def name(self):
        return self.__class__.__name__

    @abc.abstractclassmethod
    def preprocess(self, clip: AudioClip):
        raise NotImplementedError()

    @abc.abstractmethod
    def classify(self) -> List[Prediction]:
        raise NotImplementedError()


class AudioLoader(abc.ABC):

    @abc.abstractmethod
    def load(self, uri) -> AudioClip:
        pass
