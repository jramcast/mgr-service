import abc
from ..domain.entities import AudioClip


class Model(abc.ABC):

    @property
    def name(self):
        return self.__class__.__name__

    @abc.abstractclassmethod
    def preprocess(self, clip: AudioClip):
        raise NotImplementedError()

    @abc.abstractmethod
    def classify(self):
        raise NotImplementedError()
