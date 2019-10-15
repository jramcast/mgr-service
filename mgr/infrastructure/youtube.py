import math
import pafy
import subprocess as sp
import os
from scipy.io.wavfile import read
from ..usecases.classify import AudioLoader
from ..domain.entities import AudioClip


class YoutubeAudioLoader(AudioLoader):

    def load(self, uri) -> AudioClip:
        video = pafy.new(uri)
        audio_url = _get_audio_url(video)
        return _download_raw_audio(video, audio_url)
        return AudioClip(video.length)


def download(video_page_url):
    # Get the direct URLs to the videos with best audio and with best video (with audio)
    video = pafy.new(video_page_url)
    print("VIDEO", video)

    audio_url = _get_audio_url(video)

    return _download_raw_audio(video, audio_url)


def _get_audio_url(video):
    best_audio = video.getbestaudio()
    best_audio_url = best_audio.url
    print("Audio URL: " + best_audio_url)
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
    audio_dl_args = ['ffmpeg',
        '-ss', str(0),           # The beginning of the trim window
        '-i', url,               # Specify the input video URL
        '-t', str(video.length), # Specify the duration of the output
        '-y',                    # Override file if exists
        '-vn',                   # Suppress the video stream
        '-ac', '2',              # Set the number of channels
        '-sample_fmt', 's16',    # Specify the bit depth
        '-acodec', audio_codec,  # Specify the output encoding
        '-ar', '44100',          # Specify the audio sample rate
        audio_filepath]

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
        '-segment_time', str(SEGMENT_SECONDS),    # Specify the segment duration
        '-c', 'copy',  # Specify the output encoding
        segment_audio_filepath
    ]

    proc = sp.Popen(audio_dl_args, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        print("ERROR", stderr)
    else:
        print("Splitted" + segment_audio_filepath)

    return basename_fmt
