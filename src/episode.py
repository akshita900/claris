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


def load_claris_episode(
    record_path: str,
    record_id: str,
    event: str,
    decision: Optional[bool] = None,
) -> CLARISEpisode:
    """
    Load a local WFDB record and construct a CLARIS episode.
    """

    import wfdb
    from pathlib import Path

    record_path = Path(record_path)

    # Validate that the local VTaC waveform files exist.
    if not record_path.with_suffix(".hea").exists():
        raise FileNotFoundError(
            f"VTaC waveform header not found: "
            f"{record_path.with_suffix('.hea')}"
        )

    if not record_path.with_suffix(".dat").exists():
        raise FileNotFoundError(
            f"VTaC waveform data file not found: "
            f"{record_path.with_suffix('.dat')}"
        )

    # Load the WFDB waveform record.
    record = wfdb.rdrecord(str(record_path))

    # VTaC alarm onset occurs at 300 seconds.
    alarm_sample = int(300 * record.fs)

    # Alarm-centered time axis:
    # -300 seconds before alarm → 0 at alarm → +60 seconds after alarm.
    time = (
        np.arange(record.sig_len) - alarm_sample
    ) / record.fs

    return CLARISEpisode(
        record=record_id,
        event=event,
        sampling_frequency=record.fs,
        n_samples=record.sig_len,
        duration_seconds=record.sig_len / record.fs,
        alarm_sample=alarm_sample,
        signals=record.sig_name,
        waveform=record.p_signal,
        time=time,
        units=record.units,
        decision=decision,
    )
def load_available_claris_episodes(
    event_table,
    raw_dir: str,
) -> tuple[list[CLARISEpisode], list[str]]:
    """
    Load all VTaC episodes whose waveform files are available locally.

    Returns:
        episodes: successfully loaded CLARIS episodes
        missing_events: event IDs whose waveform files are not available
    """

    from pathlib import Path

    raw_dir = Path(raw_dir)

    episodes = []
    missing_events = []

    for _, row in event_table.iterrows():
        record_id = row["record"]
        event_id = row["event"]
        decision = row["decision"]

        record_path = raw_dir / event_id

        if not record_path.with_suffix(".hea").exists():
            missing_events.append(event_id)
            continue

        if not record_path.with_suffix(".dat").exists():
            missing_events.append(event_id)
            continue

        episode = load_claris_episode(
            record_path=str(record_path),
            record_id=record_id,
            event=event_id,
            decision=decision,
        )

        episodes.append(episode)

    return episodes, missing_events