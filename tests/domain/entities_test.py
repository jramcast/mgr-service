from mgr.domain.entities import AudioClip, AudioSegment


def test_audio_returns_the_right_number_of_segments():
    length_seconds = 65

    clip = AudioClip(length_seconds)

    assert len(clip.segments) == 7


def test_audio_returns_correct_segments():
    length_seconds = 65

    clip = AudioClip(length_seconds)

    assert clip.segments[0] == AudioSegment(0, 0, 10)
    assert clip.segments[1] == AudioSegment(1, 10, 20)
    assert clip.segments[6] == AudioSegment(6, 60, 65)
