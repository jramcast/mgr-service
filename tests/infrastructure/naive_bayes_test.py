from mgr.infrastructure.models.naivebayes import NaiveBayesModel
from mgr.domain.entities import AudioClip


def test_naive_bayes_model():
    model = NaiveBayesModel()

    clip = AudioClip("./tests/infrastructure/test.wav", 2)
    x = model.preprocess(clip)
    result = model.classify(x)

    assert result == ""