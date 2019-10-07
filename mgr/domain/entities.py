from typing import List
from dataclasses import dataclass


@dataclass
class PredictionResult:
    labels: List[str]


class ModelInputFeatures:
    pass
