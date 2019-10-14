import math
from typing import List
from dataclasses import dataclass


@dataclass
class PredictedLabel:
    name: str
    score: float


@dataclass
class ClassificationResult:
    labels: List[PredictedLabel]


class ModelInputFeatures:
    pass


@dataclass
class AudioSegment:
    order: int
    start: float
    stop: float


class AudioClip:

    segments: List[AudioSegment]
    length_seconds: int
    segment_seconds: int

    def __init__(self, length_seconds, segment_seconds=10):
        self.length_seconds = length_seconds
        self.segment_seconds = segment_seconds
        self.segments = self.calculate_segments()

    def calculate_segments(self):
        num_segments = math.ceil(self.length_seconds / self.segment_seconds)

        segments = []
        for i in range(0, num_segments):
            start = i * self.segment_seconds
            stop = start + self.segment_seconds
            if stop > self.length_seconds:
                stop = self.length_seconds
            segments.append(
                AudioSegment(i, start, stop)
            )
        return segments
