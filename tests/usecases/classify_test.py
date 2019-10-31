from mgr.usecases.interfaces import Model
from mgr.usecases.classify import ClassifyUseCase
from mgr.usecases.interfaces import AudioLoader
from mgr.domain.entities import (Prediction, AudioClip, AudioSegment)


def test_predict_returns_predictions():
    models = {
        "fakeModel": FakeModel()
    }
    usecase = ClassifyUseCase(models, FakeAudioLoader())

    inputdata = "youtube.com/1234"
    result = usecase.run(inputdata, model_id="fakeModel")
    assert {
        "FakeModel": [
            [{
                "label": "ball",
                "score": 0.84
            }]
        ]
    } == result


class FakeAudioLoader(AudioLoader):

    def load(self, uri):
        return AudioClip("test.wav", 60)

    def load_segment(self, uri):
        return AudioSegment("test_000.wav", start=0, stop=10)


class FakeModel(Model):

    def preprocess(self, clip: AudioClip):
        return []

    def classify(self, data):
        return [[Prediction("ball", 0.84)]]
