import os
import subprocess as sp
from dataclasses import dataclass

import pafy
from ..usecases.interfaces import AudioLoader, Cache
from ..domain.entities import AudioClip, AudioSegment


@dataclass
class VideoInfo:
    id: str
    audio_url: str
    length: int


class YoutubeAudioLoader(AudioLoader):

    def __init__(self, cache: Cache[VideoInfo]):
        self.cache = cache

    def load(self, uri) -> AudioClip:
        """
        Downloads a full youtube clip and splits it in segments
        """
        videoinfo = self._get_video_info(uri)
        filepath = _download_raw_audio(videoinfo)
        return AudioClip(filepath, videoinfo.length)

    def load_segment(self, uri, from_second, duration=10):
        """
        Downloads a segment from a youtube clip
        """
        videoinfo = self._get_video_info(uri)
        filepath = _download_raw_audio_segment(
            videoinfo, from_second, duration)
        return AudioSegment(filepath, from_second, from_second + duration)

    def _get_video_info(self, uri: str) -> VideoInfo:
        videoinfo = self.cache.get(uri)
        print(":::" * 500)
        print("Videoinfo from cache", videoinfo)
        if videoinfo is None:
            video = pafy.new(uri)
            audio_url = _get_audio_url(video)
            videoinfo = VideoInfo(
                video.videoid,
                audio_url,
                video.length
            )
            self.cache.set(uri, videoinfo)
        return videoinfo


def _get_audio_url(video):
    best_audio = video.getbestaudio()
    best_audio_url = best_audio.url
    return best_audio_url


def _download_raw_audio(videoinfo: VideoInfo):

    # Set output settings
    audio_codec = 'pcm_s16le'
    audio_container = 'wav'

    # Get output video and audio filepaths
    base_path = './.tmp/'

    basename_fmt = videoinfo.id
    audio_filepath = os.path.join(
        base_path, basename_fmt + '.' + audio_container
    )

    # Download the audio
    audio_dl_args = [
        'ffmpeg',
        '-ss', str(0),            # The beginning of the trim window
        '-i', videoinfo.audio_url,  # Specify the input video URL
        '-t', str(videoinfo.length),  # Specify the duration of the output
        '-y',                      # Override file if exists
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

    SEGMENT_SECONDS = 10
    # for i in range(math.floor(video.length / SEGMENT_SECONDS)):

    #     start = i * SEGMENT_SECONDS
    #     end = start + SEGMENT_SECONDS
    basename_segment_fmt = "{}_%03d".format(videoinfo.id)
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


def _download_raw_audio_segment(videoinfo: VideoInfo, from_second, duration):

    # Set output settings
    audio_codec = 'pcm_s16le'
    audio_container = 'wav'

    # Get output video and audio filepaths
    base_path = './.tmp/'

    basename_fmt = "{}_from_{}".format(videoinfo.id, from_second)
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
        '-i', videoinfo.audio_url,  # Specify the input video URL
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


class VideoInfoCacheInMemory(Cache[VideoInfo]):

    def __init__(self):
        self.storage = {}

    def get(self, key: str) -> VideoInfo:
        return self.storage.get(key)

    def set(self, key: str, entry: VideoInfo):
        self.storage[key] = entry

    def __contains__(self, key: str) -> bool:
        return key in self.storage
