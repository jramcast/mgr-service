from mgr.infrastructure import youtube
from mgr.infrastructure import embeddings
from mgr.infrastructure.ontology import MUSIC_GENRE_CLASSES


import numpy as np
from joblib import load


def test_youtube_audio_donwload():
    # Nirvana - Come As You Are
    filename = youtube.download("https://www.youtube.com/watch?v=vabnZ9-ex7o")

    sample = embeddings.extract(".tmp/{}_002.wav".format(filename))
    assert sample.shape == (10, 128)

    model = load("./mgr/infrastructure/models/bal_bayes.joblib")

    flattened_sample = np.array(sample).reshape(-1, 1280)
    result = model.predict(flattened_sample)
    result_probs = model.predict_proba(flattened_sample)

    predictions = []

    # TODO: embed this in use case
    for i, prediction in enumerate(result[0]):
        if prediction == 1:
            predictions.append({
                "genre": MUSIC_GENRE_CLASSES[i]["name"],
                "probability": result_probs[0][i]
            })

    assert len(predictions) > 0
    genres = [prediction["genre"] for prediction in predictions]
    assert "Grunge" in genres
    assert "Rock music" in genres
    assert "Rock and roll" in genres
