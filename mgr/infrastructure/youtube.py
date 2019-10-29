import os
import subprocess as sp
import pafy
from ..usecases.interfaces import AudioLoader
from ..domain.entities import AudioClip, AudioSegment


class YoutubeAudioLoader(AudioLoader):

    def load(self, uri) -> AudioClip:
        video = pafy.new(uri)
        audio_url = _get_audio_url(video)
        filepath = _download_raw_audio(video, audio_url)
        return AudioClip(filepath, video.length)

    def load_segment(self, uri, from_second):
        video = pafy.new(uri)
        audio_url = _get_audio_url(video)
        duration = 10
        print("downloading segment: ", uri, from_second)
        filepath = _download_raw_audio_segment(
            video, audio_url, from_second, duration)
        print("segment downloaded: ", filepath)
        return AudioSegment(filepath, from_second, from_second + duration)


def download(video_page_url):
    # Get the direct URLs to the videos with best audio and with best video (with audio)
    video = pafy.new(video_page_url)
    audio_url = _get_audio_url(video)
    return _download_raw_audio(video, audio_url)


def _get_audio_url(video):
    best_audio = video.getbestaudio()
    best_audio_url = best_audio.url
    return best_audio_url


def _download_raw_audio(video, url):

    print("DOWNLOADING AUDIO.")

    # Set output settings
    audio_codec = 'pcm_s16le'
    audio_container = 'wav'

    # Get output video and audio filepaths
    base_path = './.tmp/'

    basename_fmt = video.videoid
    audio_filepath = os.path.join(
        base_path, basename_fmt + '.' + audio_container
    )

    # Download the audio
    audio_dl_args = [
        'ffmpeg',
        '-ss', str(0),            # The beginning of the trim window
        '-i', url,                # Specify the input video URL
        '-t', str(video.length),  # Specify the duration of the output
        '-y',                     # Override file if exists
        '-vn',                    # Suppress the video stream
        '-ac', '2',               # Set the number of channels
        '-sample_fmt', 's16',     # Specify the bit depth
        '-acodec', audio_codec,   # Specify the output encoding
        '-ar', '44100',           # Specify the audio sample rate
        audio_filepath
    ]

    proc = sp.Popen(audio_dl_args, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        print(stderr)
    else:
        print("Downloaded audio to " + audio_filepath)


    print("Video length seconds", video.length)

    SEGMENT_SECONDS = 10
    # for i in range(math.floor(video.length / SEGMENT_SECONDS)):

    #     start = i * SEGMENT_SECONDS
    #     end = start + SEGMENT_SECONDS
    basename_segment_fmt = "{}_%03d".format(video.videoid)
    segment_audio_filepath = os.path.join(
        base_path, basename_segment_fmt + '.' + audio_container
    )

    # Download the audio
    audio_dl_args = [
        'ffmpeg',
        '-i', audio_filepath,       # Specify the input video URL
        '-f', 'segment',            # Segment the file
        '-y',                       # Override file if exists
        '-segment_time', str(SEGMENT_SECONDS),  # Specify the segment duration
        '-c', 'copy',  # Specify the output encoding
        segment_audio_filepath
    ]

    proc = sp.Popen(audio_dl_args, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        print("ERROR", stderr)
    else:
        print("Splitted" + segment_audio_filepath)

    return audio_filepath


def _download_raw_audio_segment(video, url, from_second, duration):

    print("DOWNLOADING AUDIO.")

    # Set output settings
    audio_codec = 'pcm_s16le'
    audio_container = 'wav'

    # Get output video and audio filepaths
    base_path = './.tmp/'

    basename_fmt = "{}_from_{}".format(video.videoid, from_second)
    audio_filepath = os.path.join(
        base_path, basename_fmt + '.' + audio_container
    )

    if os.path.exists(audio_filepath):
        print("File already exists")
        return audio_filepath

    # Download the audio
    audio_dl_args = [
        'ffmpeg',
        '-ss', str(from_second),    # The beginning of the trim window
        '-i', url,                  # Specify the input video URL
        '-t', str(duration),        # Specify the duration of the output
        '-y',                     # Override file if exists
        '-vn',                    # Suppress the video stream
        '-ac', '2',               # Set the number of channels
        '-sample_fmt', 's16',     # Specify the bit depth
        '-acodec', audio_codec,   # Specify the output encoding
        '-ar', '44100',           # Specify the audio sample rate
        audio_filepath
    ]

    proc = sp.Popen(audio_dl_args, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        print(stderr)
    else:
        print("Downloaded audio to " + audio_filepath)

    return audio_filepath