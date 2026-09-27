import numpy as np


def validate_episode_waveform(
    waveform: np.ndarray,
    sampling_frequency: float,
    expected_samples: int,
) -> dict:
    """
    Validate the basic structural integrity of a CLARIS waveform.

    This function performs validation only.
    It does not filter, normalize, resample, or modify the waveform.
    """

    waveform = np.asarray(waveform)

    if waveform.ndim != 2:
        raise ValueError(
            "Waveform must be a 2D array: samples × signals."
        )

    if waveform.shape[0] != expected_samples:
        raise ValueError(
            f"Expected {expected_samples} samples, "
            f"but received {waveform.shape[0]}."
        )

    if sampling_frequency <= 0:
        raise ValueError(
            "Sampling frequency must be greater than zero."
        )

    finite_mask = np.isfinite(waveform)

    return {
        "valid_shape": True,
        "n_samples": int(waveform.shape[0]),
        "n_signals": int(waveform.shape[1]),
        "sampling_frequency": float(sampling_frequency),
        "all_values_finite": bool(finite_mask.all()),
        "nan_count": int(np.isnan(waveform).sum()),
        "inf_count": int(np.isinf(waveform).sum()),
    }