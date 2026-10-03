from pathlib import Path
import json
import sys

import numpy as np
from scipy.signal import find_peaks, butter, filtfilt


# ============================================================
# CLARIS - Physiological Evidence Extraction
# Phase 2.4
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJECT_ROOT / "src"
EPISODE_DIR = PROJECT_ROOT / "data" / "episodes"

sys.path.insert(0, str(SRC_DIR))


# ============================================================
# Load episode
# ============================================================

def load_episode(event_name):

    episode_path = EPISODE_DIR / event_name

    metadata_path = episode_path / "metadata.json"
    waveform_path = episode_path / "waveforms.npz"

    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    waveform_data = np.load(waveform_path)

    pre_event = waveform_data["pre_event"]
    post_event = waveform_data["post_event"]

    waveforms = np.vstack(
        (pre_event, post_event)
    )

    return metadata, waveforms


# ============================================================
# Filtering
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
# ECG R-peak detection
# ============================================================

def detect_ecg_r_peaks(
    signal,
    sampling_frequency
):
    """
    Conservative ECG R-peak detector.

    This is an interpretable first-pass detector.
    It is not a diagnostic algorithm.
    """

    filtered = bandpass_filter(
        signal,
        sampling_frequency,
        lowcut=5.0,
        highcut=18.0
    )

    # --------------------------------------------------------
    # Estimate robust signal scale
    # --------------------------------------------------------

    median_value = np.median(filtered)

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

    # --------------------------------------------------------
    # Candidate R peaks
    # --------------------------------------------------------

    minimum_distance = int(
        0.30 * sampling_frequency
    )

    prominence = 2.0 * robust_scale

    peaks, properties = find_peaks(
        filtered,
        distance=minimum_distance,
        prominence=prominence
    )

    # --------------------------------------------------------
    # Additional amplitude screening
    # --------------------------------------------------------

    peak_values = filtered[peaks]

    amplitude_threshold = (
        np.percentile(
            peak_values,
            60
        )
        if len(peak_values) > 0
        else 0
    )

    valid_mask = (
        peak_values >= amplitude_threshold
    )

    peaks = peaks[valid_mask]

    return filtered, peaks


# ============================================================
# ECG features
# ============================================================

def extract_ecg_features(
    signal,
    sampling_frequency,
    alarm_sample
):

    filtered, peaks = detect_ecg_r_peaks(
        signal,
        sampling_frequency
    )

    peak_times = (
        peaks / sampling_frequency
    )

    # --------------------------------------------------------
    # RR intervals
    # --------------------------------------------------------

    if len(peaks) >= 2:

        rr_intervals = np.diff(
            peak_times
        )

        # Keep physiologically plausible intervals
        valid_rr = rr_intervals[
            (rr_intervals >= 0.25)
            &
            (rr_intervals <= 2.0)
        ]

        if len(valid_rr) > 0:

            heart_rates = (
                60.0 / valid_rr
            )

            mean_rr = float(
                np.mean(valid_rr)
            )

            std_rr = float(
                np.std(valid_rr)
            )

            mean_heart_rate = float(
                np.mean(heart_rates)
            )

        else:

            mean_rr = None
            std_rr = None
            mean_heart_rate = None

    else:

        mean_rr = None
        std_rr = None
        mean_heart_rate = None

    # --------------------------------------------------------
    # Local alarm window
    # --------------------------------------------------------

    alarm_time = (
        alarm_sample /
        sampling_frequency
    )

    start_time = (
        alarm_time - 5.0
    )

    end_time = (
        alarm_time + 5.0
    )

    local_mask = (
        (peak_times >= start_time)
        &
        (peak_times <= end_time)
    )

    local_peaks = peaks[
        local_mask
    ]

    return {
        "peak_count":
            int(len(peaks)),

        "peak_times_seconds":
            peak_times.tolist(),

        "local_peak_count":
            int(len(local_peaks)),

        "mean_rr_seconds":
            mean_rr,

        "std_rr_seconds":
            std_rr,

        "mean_heart_rate_bpm":
            mean_heart_rate,

        "filtered_signal_std":
            float(np.std(filtered)),
    }


# ============================================================
# PLETH peak detection
# ============================================================

def detect_pleth_peaks(
    signal,
    sampling_frequency
):

    filtered = bandpass_filter(
        signal,
        sampling_frequency,
        lowcut=0.5,
        highcut=5.0
    )

    signal_std = np.std(filtered)

    if signal_std == 0:
        signal_std = 1.0

    minimum_distance = int(
        0.35 * sampling_frequency
    )

    prominence = 0.3 * signal_std

    peaks, _ = find_peaks(
        filtered,
        distance=minimum_distance,
        prominence=prominence
    )

    return filtered, peaks


# ============================================================
# PLETH features
# ============================================================

def extract_pleth_features(
    signal,
    sampling_frequency,
    alarm_sample
):

    filtered, peaks = detect_pleth_peaks(
        signal,
        sampling_frequency
    )

    peak_times = (
        peaks / sampling_frequency
    )

    if len(peaks) >= 2:

        pulse_intervals = np.diff(
            peak_times
        )

        valid_intervals = pulse_intervals[
            (pulse_intervals >= 0.35)
            &
            (pulse_intervals <= 2.0)
        ]

        if len(valid_intervals) > 0:

            pulse_rates = (
                60.0 /
                valid_intervals
            )

            mean_pulse_interval = float(
                np.mean(valid_intervals)
            )

            mean_pulse_rate = float(
                np.mean(pulse_rates)
            )

        else:

            mean_pulse_interval = None
            mean_pulse_rate = None

    else:

        mean_pulse_interval = None
        mean_pulse_rate = None

    # --------------------------------------------------------
    # Local alarm window
    # --------------------------------------------------------

    alarm_time = (
        alarm_sample /
        sampling_frequency
    )

    start_time = (
        alarm_time - 5.0
    )

    end_time = (
        alarm_time + 5.0
    )

    local_mask = (
        (peak_times >= start_time)
        &
        (peak_times <= end_time)
    )

    local_peaks = peaks[
        local_mask
    ]

    return {
        "peak_count":
            int(len(peaks)),

        "peak_times_seconds":
            peak_times.tolist(),

        "local_peak_count":
            int(len(local_peaks)),

        "mean_pulse_interval_seconds":
            mean_pulse_interval,

        "mean_pulse_rate_bpm":
            mean_pulse_rate,

        "filtered_signal_std":
            float(np.std(filtered)),
    }


# ============================================================
# Main feature extraction
# ============================================================

def extract_physiological_features(
    metadata,
    waveforms
):

    sampling_frequency = metadata[
        "sampling_frequency_hz"
    ]

    alarm_sample = metadata[
        "event_window"
    ][
        "alarm_reference_sample"
    ]

    signal_names = list(
        metadata["signals"].keys()
    )

    results = {}

    for index, signal_name in enumerate(
        signal_names
    ):

        signal = waveforms[:, index]

        modality = metadata[
            "signals"
        ][
            signal_name
        ][
            "modality"
        ]

        if modality == "ECG":

            features = extract_ecg_features(
                signal,
                sampling_frequency,
                alarm_sample
            )

        elif modality == "PPG":

            features = extract_pleth_features(
                signal,
                sampling_frequency,
                alarm_sample
            )

        else:

            features = {
                "status":
                    "No feature extractor implemented."
            }

        results[signal_name] = {
            "modality": modality,
            "features": features
        }

    return results


# ============================================================
# Save
# ============================================================

def save_features(
    event_name,
    results
):

    episode_path = (
        EPISODE_DIR / event_name
    )

    output_path = (
        episode_path /
        "physiological_features.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    return output_path


# ============================================================
# Summary
# ============================================================

def print_summary(
    results,
    output_path
):

    print("\n========================================")
    print("CLARIS - Physiological Evidence")
    print("========================================")

    for signal_name, result in results.items():

        print(
            f"\nSignal: {signal_name}"
        )

        print(
            f"Modality: "
            f"{result['modality']}"
        )

        features = result["features"]

        if result["modality"] == "ECG":

            print(
                f"  Detected R-peaks: "
                f"{features['peak_count']}"
            )

            print(
                f"  Local R-peaks ±5 s: "
                f"{features['local_peak_count']}"
            )

            print(
                f"  Mean RR: "
                f"{features['mean_rr_seconds']}"
            )

            print(
                f"  RR standard deviation: "
                f"{features['std_rr_seconds']}"
            )

            print(
                f"  Mean heart rate: "
                f"{features['mean_heart_rate_bpm']}"
            )

        elif result["modality"] == "PPG":

            print(
                f"  Detected pulses: "
                f"{features['peak_count']}"
            )

            print(
                f"  Local pulses ±5 s: "
                f"{features['local_peak_count']}"
            )

            print(
                f"  Mean pulse interval: "
                f"{features['mean_pulse_interval_seconds']}"
            )

            print(
                f"  Mean pulse rate: "
                f"{features['mean_pulse_rate_bpm']}"
            )

    print("\n----------------------------------------")
    print("Saved to:")
    print(output_path)

    print("\n========================================")
    print("Physiological feature extraction complete.")
    print("========================================")


# ============================================================
# Main
# ============================================================

def main():

    event_name = "003c13_0115"

    metadata, waveforms = load_episode(
        event_name
    )

    results = extract_physiological_features(
        metadata,
        waveforms
    )

    output_path = save_features(
        event_name,
        results
    )

    print_summary(
        results,
        output_path
    )


if __name__ == "__main__":
    main()