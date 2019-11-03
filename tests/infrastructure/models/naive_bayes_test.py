from mgr.infrastructure.models.naivebayes import NaiveBayesModel
from mgr.domain.entities import AudioClip, Prediction


def test_naive_bayes_model():
    model = NaiveBayesModel()

    clip = AudioClip("./tests/infrastructure/test.wav", 2)
    x = model.preprocess(clip.segments)
    predictions = model.classify(x)

    assert predictions == [
        [
            Prediction("Beatboxing", score=0.5691070272850726),
            Prediction("Beatboxing", score=0.5691070272850726)
        ]
    ]
