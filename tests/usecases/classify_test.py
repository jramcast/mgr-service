from mgr.usecases.interfaces import Model
from mgr.usecases.classify import ClassifyUseCase
from mgr.domain.entities import ClassificationResult, PredictedLabel


class TestDummy:

    def test_predict_returns_predictions(self):
        models = [FakeModel()]
        usecase = ClassifyUseCase(models, {})

        inputdata = "youtube.com/1234"
        result = usecase.run(inputdata)
        assert result == [
            [{
                "label": "ball",
                "score": 0.84
            }]
        ]


class FakeModel(Model):

    def classify(self, data):
        return ClassificationResult(
            [PredictedLabel("ball", 0.84)]
        )
