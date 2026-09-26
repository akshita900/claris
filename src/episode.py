from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class CLARISEpisode:
    record: str
    event: str
    sampling_frequency: float
    n_samples: int
    duration_seconds: float
    alarm_sample: int
    signals: list[str]
    waveform: Optional[np.ndarray] = None
    time: Optional[np.ndarray] = None
    units: Optional[list[str]] = None
    decision: Optional[bool] = None