from mgr.infrastructure import youtube
from mgr.infrastructure import embeddings


def test_youtube_audio_donwload():
    filepaths = list(youtube.download("https://www.youtube.com/watch?v=_FG695geZVM"))

    sample = embeddings.extract(filepaths[0])
    assert sample.shape == (10, 128)
