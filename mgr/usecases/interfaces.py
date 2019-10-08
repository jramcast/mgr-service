import abc


class Model(abc.ABC):

    @abc.abstractmethod
    def classify(self):
        raise NotImplementedError()
