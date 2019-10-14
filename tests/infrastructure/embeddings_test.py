from mgr.infrastructure import embeddings


def test_extract_vggish_embeddings_from_wav_file():
    audiofile_path = "tests/infrastructure/test.wav"
    sample = embeddings.extract(audiofile_path)
    assert sample.shape == (10, 128)
