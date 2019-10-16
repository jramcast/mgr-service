from mgr.usecases.interfaces import Model
from mgr.usecases.classify import ClassifyUseCase
from mgr.usecases.interfaces import AudioLoader
from mgr.domain.entities import ClassificationResult, PredictedLabel, AudioClip


class TestDummy:

    def test_predict_returns_predictions(self):
        models = [FakeModel()]
        usecase = ClassifyUseCase(models, FakeAudioLoader())

        inputdata = "youtube.com/1234"
        result = usecase.run(inputdata)
        assert result == {
            "FakeModel": [{
                "label": "ball",
                "score": 0.84
            }]
        }


class FakeAudioLoader(AudioLoader):

    def load(self, uri):
        return AudioClip("test.wav", 60)


class FakeModel(Model):

    def preprocess(self, clip: AudioClip):
        return []

    def classify(self, data):
        return ClassificationResult(
            [PredictedLabel("ball", 0.84)]
        )
