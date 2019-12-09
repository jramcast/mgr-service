import os
import logging
import subprocess as sp
from dataclasses import dataclass
from typing import List

import pafy
from ..usecases.interfaces import AudioLoader, Cache
from ..domain.entities import AudioClip, AudioSegment


@dataclass
class VideoInfo:
    """
    Necessary info to download audio files
    """
    id: str
    audio_url: str
    length: int


class YoutubeAudioLoader(AudioLoader):

    logger: logging.Logger

    def __init__(
        self,
        cache: Cache[VideoInfo],
        logger: logging.Logger,
        proxies: List[str] = [],
        max_retries=2
    ):
        self.cache = cache
        self.logger = logger
        self.proxies = [None] + proxies  # First is direct download (no proxy)
        self.max_retries = max_retries
        self.current_proxy_idx = 0
        self.current_proxy = None

    def load(self, uri) -> AudioClip:
        """
        Downloads a full youtube clip and splits it in segments
        """
        videoinfo = self._get_videoinfo(uri)
        filepath = _download_raw_audio(videoinfo, self.current_proxy)
        return AudioClip(filepath, videoinfo.length)

    def load_segment(self, uri, from_second, duration=10):
        """
        Downloads a segment from a youtube clip
        """
        videoinfo = self._get_videoinfo(uri)
        filepath = _download_raw_audio_segment(
            videoinfo, from_second, duration, self.current_proxy)
        return AudioSegment(filepath, from_second, from_second + duration)

    def _get_videoinfo(self, uri: str) -> VideoInfo:
        videoinfo = self.cache.get(uri)
        if True or videoinfo is None:
            self.logger.debug(
                "Video info retrieved from youtube (MISS): %s", uri)
            videoinfo = self._load_videoinfo_with_retry(uri)
            self.cache.set(uri, videoinfo)
        else:
            self.logger.debug("Video info retrieved from cache (HIT): %s", uri)
        return videoinfo

    def _load_videoinfo_with_retry(self, uri: str, retry=0) -> VideoInfo:
        self.current_proxy_idx += retry
        proxy_idx = self.current_proxy_idx % len(self.proxies)
        proxy = self.proxies[proxy_idx]
        self.current_proxy = proxy

        if proxy:
            youtube_dl_opts = {"proxy": proxy}
        else:
            youtube_dl_opts = {}

        try:
            video = pafy.new(uri, basic=False, ydl_opts=youtube_dl_opts)
            self.logger.debug(
                "Downloading video: %s. Proxy: %s. Retry %d",
                uri,
                proxy,
                retry
            )
            audio_url = _get_audio_url(video)
            return VideoInfo(
                video.videoid,
                audio_url,
                video.length
            )
        except Exception as err:
            if retry + 1 < self.max_retries:
                return self._load_with_retry(uri, retry + 1)
            else:
                raise err


def _get_audio_url(video):
    best_audio = video.getbestaudio()
    best_audio_url = best_audio.url
    return best_audio_url


def _download_raw_audio(videoinfo: VideoInfo, proxy=None):

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

    env = os.environ.copy()
    if proxy:
        env["http_proxy"] = proxy
    proc = sp.Popen(audio_dl_args, stdout=sp.PIPE, stderr=sp.PIPE, env=env)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        print("ERROR", stderr)
    else:
        print("Splitted" + segment_audio_filepath)

    return audio_filepath


def _download_raw_audio_segment(
    videoinfo: VideoInfo, from_second, duration, proxy=None
):
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
        print(
            "Segment file exists in disk %s. Skipping download",
            videoinfo.id)
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

    env = os.environ.copy()
    if proxy:
        env["http_proxy"] = proxy
    proc = sp.Popen(audio_dl_args, stdout=sp.PIPE, stderr=sp.PIPE, env=env)
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
