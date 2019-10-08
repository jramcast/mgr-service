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
