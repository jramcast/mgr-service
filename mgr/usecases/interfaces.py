import abc
from typing import List, TypeVar, Generic
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


# Todo, have only 1 cache class
class FeaturesCache(abc.ABC):

    @abc.abstractmethod
    def get(self, key: str):
        pass

    @abc.abstractmethod
    def set(self, key: str, entry):
        pass

    @abc.abstractmethod
    def __contains__(self, key: str) -> bool:
        pass


T = TypeVar('T')


class Cache(abc.ABC, Generic[T]):

    @abc.abstractmethod
    def get(self, key: str) -> T:
        pass

    @abc.abstractmethod
    def set(self, key: str, entry: T):
        pass

    @abc.abstractmethod
    def __contains__(self, key: str) -> bool:
        pass
