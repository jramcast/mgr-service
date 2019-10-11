from mgr.infrastructure import youtube
from mgr.infrastructure import embeddings
from mgr.infrastructure.ontology import MUSIC_GENRE_CLASSES


import numpy as np
from joblib import load


def test_youtube_audio_donwload():
    filename = youtube.download("https://www.youtube.com/watch?v=YuBeBjqKSGQ")

    sample = embeddings.extract(".tmp/{}_000.wav".format(filename))
    assert sample.shape == (10, 128)

    model = load("./mgr/infrastructure/models/bal_bayes.joblib")

    flattened_sample = np.array(sample).reshape(-1, 1280)
    result = model.predict(flattened_sample)
    result_probs = model.predict_proba(flattened_sample)

    predictions = []
    for i, prediction in enumerate(result[0]):
        if prediction == 1:
            predictions.append({
                "genre": MUSIC_GENRE_CLASSES[i]["name"],
                "probability": result_probs[0][i]
            })

    from pprint import pprint
    pprint(predictions)
    assert predictions == (1, 53)
