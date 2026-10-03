from pathlib import Path
import json

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt


# ============================================================
# CLARIS - Feature Validation
# Phase 2.4
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODE_DIR = PROJECT_ROOT / "data" / "episodes"


# ============================================================
# Load episode
# ============================================================

def load_episode(event_name):

    episode_path = EPISODE_DIR / event_name

    with open(
        episode_path / "metadata.json",
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(file)

    waveform_data = np.load(
        episode_path / "waveforms.npz"
    )

    waveforms = np.vstack(
        (
            waveform_data["pre_event"],
            waveform_data["post_event"]
        )
    )

    return metadata, waveforms


# ============================================================
# Filter
# ============================================================

def bandpass_filter(
    signal,
    sampling_frequency,
    lowcut,
    highcut,
    order=3
):

    nyquist = 0.5 * sampling_frequency

    low = lowcut / nyquist
    high = highcut / nyquist

    b, a = butter(
        order,
        [low, high],
        btype="band"
    )

    return filtfilt(
        b,
        a,
        signal
    )


# ============================================================
# ECG detector
# ============================================================

def detect_ecg_r_peaks(
    signal,
    sampling_frequency
):

    filtered = bandpass_filter(
        signal,
        sampling_frequency,
        5.0,
        18.0
    )

    median_value = np.median(
        filtered
    )

    absolute_deviation = np.abs(
        filtered - median_value
    )

    robust_scale = np.median(
        absolute_deviation
    )

    if robust_scale == 0:
        robust_scale = np.std(filtered)

    if robust_scale == 0:
        robust_scale = 1.0

    minimum_distance = int(
        0.30 * sampling_frequency
    )

    prominence = (
        2.0 * robust_scale
    )

    peaks, _ = find_peaks(
        filtered,
        distance=minimum_distance,
        prominence=prominence
    )

    if len(peaks) > 0:

        peak_values = filtered[peaks]

        amplitude_threshold = np.percentile(
            peak_values,
            60
        )

        peaks = peaks[
            peak_values >= amplitude_threshold
        ]

    return filtered, peaks


# ============================================================
# PLETH detector
# ============================================================

def detect_pleth_peaks(
    signal,
    sampling_frequency
):

    filtered = bandpass_filter(
        signal,
        sampling_frequency,
        0.5,
        5.0
    )

    signal_std = np.std(
        filtered
    )

    if signal_std == 0:
        signal_std = 1.0

    minimum_distance = int(
        0.35 * sampling_frequency
    )

    prominence = (
        0.3 * signal_std
    )

    peaks, _ = find_peaks(
        filtered,
        distance=minimum_distance,
        prominence=prominence
    )

    return filtered, peaks


# ============================================================
# Plot ECG
# ============================================================

def plot_ecg(
    time_axis,
    filtered,
    peaks,
    alarm_time,
    start_time,
    end_time,
    signal_name
):

    mask = (
        (time_axis >= start_time)
        &
        (time_axis <= end_time)
    )

    visible_time = time_axis[mask]
    visible_signal = filtered[mask]

    peak_times = (
        peaks / 250.0
    )

    peak_mask = (
        (peak_times >= start_time)
        &
        (peak_times <= end_time)
    )

    visible_peak_times = peak_times[
        peak_mask
    ]

    visible_peak_indices = peaks[
        peak_mask
    ]

    plt.figure(
        figsize=(12, 5)
    )

    plt.plot(
        visible_time,
        visible_signal,
        label="Filtered ECG"
    )

    plt.scatter(
        visible_peak_times,
        filtered[visible_peak_indices],
        label="Detected R-peaks",
        s=35
    )

    plt.axvline(
        alarm_time,
        linestyle="--",
        label="Alarm reference"
    )

    plt.title(
        f"CLARIS - {signal_name} "
        "R-Peak Validation"
    )

    plt.xlabel(
        "Time (seconds)"
    )

    plt.ylabel(
        "Filtered amplitude"
    )

    plt.legend()

    plt.tight_layout()

    plt.show()


# ============================================================
# Plot PLETH
# ============================================================

def plot_pleth(
    time_axis,
    filtered,
    peaks,
    alarm_time,
    sampling_frequency,
    start_time,
    end_time
):

    mask = (
        (time_axis >= start_time)
        &
        (time_axis <= end_time)
    )

    visible_time = time_axis[mask]
    visible_signal = filtered[mask]

    peak_times = (
        peaks / sampling_frequency
    )

    peak_mask = (
        (peak_times >= start_time)
        &
        (peak_times <= end_time)
    )

    visible_peak_times = peak_times[
        peak_mask
    ]

    visible_peak_indices = peaks[
        peak_mask
    ]

    plt.figure(
        figsize=(12, 5)
    )

    plt.plot(
        visible_time,
        visible_signal,
        label="Filtered PLETH"
    )

    plt.scatter(
        visible_peak_times,
        filtered[visible_peak_indices],
        label="Detected pulses",
        s=35
    )

    plt.axvline(
        alarm_time,
        linestyle="--",
        label="Alarm reference"
    )

    plt.title(
        "CLARIS - PLETH Pulse Validation"
    )

    plt.xlabel(
        "Time (seconds)"
    )

    plt.ylabel(
        "Filtered amplitude"
    )

    plt.legend()

    plt.tight_layout()

    plt.show()


# ============================================================
# Main
# ============================================================

def main():

    event_name = "003c13_0115"

    metadata, waveforms = load_episode(
        event_name
    )

    fs = metadata[
        "sampling_frequency_hz"
    ]

    alarm_sample = metadata[
        "event_window"
    ][
        "alarm_reference_sample"
    ]

    alarm_time = (
        alarm_sample / fs
    )

    signal_names = list(
        metadata["signals"].keys()
    )

    start_time = 295
    end_time = 305

    print("\n========================================")
    print("CLARIS - Feature Validation")
    print("========================================")

    print(
        f"Event: {event_name}"
    )

    print(
        f"Window: {start_time}-{end_time} seconds"
    )

    print(
        f"Alarm reference: "
        f"{alarm_time:.3f} seconds"
    )

    # --------------------------------------------------------
    # Validate all three ECG leads
    # --------------------------------------------------------

    for signal_name in [
        "II",
        "aVR",
        "V"
    ]:

        index = signal_names.index(
            signal_name
        )

        signal = waveforms[:, index]

        filtered, peaks = detect_ecg_r_peaks(
            signal,
            fs
        )

        print(
            f"{signal_name}: "
            f"{len(peaks)} detected R-peaks"
        )

        plot_ecg(
            time_axis=np.arange(
                len(signal)
            ) / fs,
            filtered=filtered,
            peaks=peaks,
            alarm_time=alarm_time,
            start_time=start_time,
            end_time=end_time,
            signal_name=signal_name
        )

    # --------------------------------------------------------
    # Validate PLETH
    # --------------------------------------------------------

    pleth_index = signal_names.index(
        "PLETH"
    )

    pleth_signal = waveforms[
        :, pleth_index
    ]

    filtered_pleth, pleth_peaks = (
        detect_pleth_peaks(
            pleth_signal,
            fs
        )
    )

    print(
        f"PLETH: "
        f"{len(pleth_peaks)} detected pulses"
    )

    plot_pleth(
        time_axis=np.arange(
            len(pleth_signal)
        ) / fs,
        filtered=filtered_pleth,
        peaks=pleth_peaks,
        alarm_time=alarm_time,
        sampling_frequency=fs,
        start_time=start_time,
        end_time=end_time
    )

    print("\n========================================")
    print("Validation complete.")
    print("========================================")


if __name__ == "__main__":
    main()