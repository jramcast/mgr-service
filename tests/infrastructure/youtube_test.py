import numpy as np
from joblib import load
from mgr.infrastructure import youtube
from mgr.infrastructure import embeddings
from mgr.infrastructure.ontology import MUSIC_GENRE_CLASSES


# TODO: limit video length
# TODO: how to handle segments. Use all? How to average results?
# TODO:


def test_youtube_audio_download():
    # Nirvana - Come As You Are
    video_id = "vabnZ9-ex7o"

    youtube.download("https://www.youtube.com/watch?v=" + video_id)

    sample = embeddings.extract(".tmp/{}_002.wav".format(video_id))
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
