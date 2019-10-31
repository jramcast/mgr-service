from mgr.infrastructure.models.neuralnetwork import NeuralNetworkModel
from mgr.domain.entities import AudioClip


def test_neural_network_model():
    model = NeuralNetworkModel()

    clip = AudioClip("./tests/infrastructure/test_new.wav", 2)
    x = model.preprocess(clip.segments)
    predictions = model.classify(x)

    predictions[0].sort(key=lambda each: -each.score)

    assert predictions[0][0].label == "Hip hop music"
