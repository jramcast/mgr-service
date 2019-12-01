from mgr.infrastructure.youtube import YoutubeAudioLoader


def test_youtube_segment_download_keeps_reference_to_tmp_file():
    # Nirvana - Come As You Are
    video_id = "vabnZ9-ex7o"

    downloader = YoutubeAudioLoader()
    segment = downloader.load_segment(video_id, 0)
    assert "./.tmp/vabnZ9-ex7o_from_0.wav" == segment.filename
