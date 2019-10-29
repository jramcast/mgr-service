import abc
from typing import List
from ..domain.entities import AudioClip, Prediction, AudioSegment


class Model(abc.ABC):

    @property
    def name(self):
        return self.__class__.__name__

    @abc.abstractclassmethod
    def preprocess(self, segments: List[AudioSegment]):
        raise NotImplementedError()

    @abc.abstractmethod
    def classify(self) -> List[List[Prediction]]:
        raise NotImplementedError()


class AudioLoader(abc.ABC):

    @abc.abstractmethod
    def load(self, uri) -> AudioClip:
        pass

    @abc.abstractmethod
    def load_segment(self, uri, from_second) -> AudioSegment:
        pass
