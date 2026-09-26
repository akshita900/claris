import numpy as np


def calculate_signal_quality_features(
    signal: np.ndarray,
    sampling_frequency: float,
    alarm_sample: int,
    window_seconds: float = 1.0,
) -> dict:
    """
    Calculate basic signal-integrity and local-behavior features
    for one physiological signal.

    This function does not assign a clinical quality label.
    It only returns measurable features.
    """

    signal = np.asarray(signal)

    # Basic data integrity
    nan_count = int(np.isnan(signal).sum())
    inf_count = int(np.isinf(signal).sum())

    # Exact repeated adjacent samples
    repeated_samples = int(np.sum(np.diff(signal) == 0))
    total_transitions = len(signal) - 1

    if total_transitions > 0:
        repeat_fraction = repeated_samples / total_transitions
    else:
        repeat_fraction = 0.0

    # Longest consecutive repeated run
    longest_run = 1
    current_run = 1

    for i in range(1, len(signal)):
        if signal[i] == signal[i - 1]:
            current_run += 1
            longest_run = max(longest_run, current_run)
        else:
            current_run = 1

    longest_repeat_duration = (
        (longest_run - 1) / sampling_frequency
    )

    # Alarm-centered local window
    window_samples = int(window_seconds * sampling_frequency)

    start = max(0, alarm_sample - window_samples)
    end = min(len(signal), alarm_sample + window_samples)

    local_segment = signal[start:end]

    local_mean = float(np.mean(local_segment))
    local_std = float(np.std(local_segment))
    local_range = float(np.ptp(local_segment))

    # Extremal-value frequency
    minimum_value = np.min(signal)
    maximum_value = np.max(signal)

    minimum_count = int(np.sum(signal == minimum_value))
    maximum_count = int(np.sum(signal == maximum_value))

    return {
        "nan_count": nan_count,
        "inf_count": inf_count,
        "repeat_fraction": float(repeat_fraction),
        "longest_repeat_samples": int(longest_run),
        "longest_repeat_duration": float(longest_repeat_duration),
        "local_mean": local_mean,
        "local_std": local_std,
        "local_range": local_range,
        "minimum_count": minimum_count,
        "maximum_count": maximum_count,
    }