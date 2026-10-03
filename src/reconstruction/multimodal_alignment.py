from pathlib import Path
import json

import numpy as np
from scipy.signal import butter, filtfilt, find_peaks


# ============================================================
# CLARIS - Multimodal Temporal Evidence
# Phase 2
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODE_DIR = PROJECT_ROOT / "data" / "episodes"


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

    filtered = bandpass_filter(
        signal,
        sampling_frequency,
        5.0,
        18.0
    )

    median_value = np.median(filtered)

    deviation = np.abs(
        filtered - median_value
    )

    robust_scale = np.median(
        deviation
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
# PLETH pulse detection
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
# Find nearest PLETH pulse after ECG beat
# ============================================================

def calculate_ecg_pleth_delays(
    ecg_peaks,
    pleth_peaks,
    sampling_frequency,
    minimum_delay=0.10,
    maximum_delay=1.00
):

    delays = []

    matched_ecg = []
    matched_pleth = []

    for ecg_peak in ecg_peaks:

        possible_pleth = pleth_peaks[
            pleth_peaks > ecg_peak
        ]

        if len(possible_pleth) == 0:
            continue

        next_pleth = possible_pleth[0]

        delay = (
            next_pleth - ecg_peak
        ) / sampling_frequency

        if (
            delay >= minimum_delay
            and
            delay <= maximum_delay
        ):

            delays.append(delay)

            matched_ecg.append(
                ecg_peak
            )

            matched_pleth.append(
                next_pleth
            )

    return (
        np.asarray(delays),
        np.asarray(matched_ecg),
        np.asarray(matched_pleth)
    )


# ============================================================
# Local event analysis
# ============================================================

def analyze_alarm_window(
    ecg_peaks,
    pleth_peaks,
    alarm_sample,
    sampling_frequency,
    window_seconds=5
):

    window_samples = int(
        window_seconds *
        sampling_frequency
    )

    start = (
        alarm_sample -
        window_samples
    )

    end = (
        alarm_sample +
        window_samples
    )

    local_ecg = ecg_peaks[
        (ecg_peaks >= start)
        &
        (ecg_peaks <= end)
    ]

    local_pleth = pleth_peaks[
        (pleth_peaks >= start)
        &
        (pleth_peaks <= end)
    ]

    delays, matched_ecg, matched_pleth = (
        calculate_ecg_pleth_delays(
            local_ecg,
            local_pleth,
            sampling_frequency
        )
    )

    result = {

        "window_seconds": window_seconds,

        "ecg_peak_count": int(
            len(local_ecg)
        ),

        "pleth_peak_count": int(
            len(local_pleth)
        ),

        "matched_beat_count": int(
            len(delays)
        ),

        "ecg_pleth_delay_mean_seconds": None,

        "ecg_pleth_delay_std_seconds": None,

        "ecg_pleth_delay_min_seconds": None,

        "ecg_pleth_delay_max_seconds": None,

        "matching_fraction": 0.0
    }

    if len(delays) > 0:

        result[
            "ecg_pleth_delay_mean_seconds"
        ] = float(
            np.mean(delays)
        )

        result[
            "ecg_pleth_delay_std_seconds"
        ] = float(
            np.std(delays)
        )

        result[
            "ecg_pleth_delay_min_seconds"
        ] = float(
            np.min(delays)
        )

        result[
            "ecg_pleth_delay_max_seconds"
        ] = float(
            np.max(delays)
        )

        if len(local_ecg) > 0:

            result[
                "matching_fraction"
            ] = float(
                len(delays) /
                len(local_ecg)
            )

    return result


# ============================================================
# Main
# ============================================================

def main():

    event_name = "003c13_0115"

    episode_path = (
        EPISODE_DIR /
        event_name
    )

    metadata_path = (
        episode_path /
        "metadata.json"
    )

    waveform_path = (
        episode_path /
        "waveforms.npz"
    )

    with open(
        metadata_path,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(file)

    waveform_data = np.load(
        waveform_path
    )

    waveforms = np.vstack(
        (
            waveform_data["pre_event"],
            waveform_data["post_event"]
        )
    )

    fs = metadata[
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

    print()
    print("=" * 40)
    print("CLARIS - Multimodal Temporal Evidence")
    print("=" * 40)

    print(
        f"Event: {event_name}"
    )

    print(
        f"Sampling frequency: {fs} Hz"
    )

    print(
        f"Alarm reference: "
        f"{alarm_sample / fs:.3f} seconds"
    )

    # --------------------------------------------------------
    # ECG reference
    # --------------------------------------------------------

    ecg_index = signal_names.index(
        "II"
    )

    pleth_index = signal_names.index(
        "PLETH"
    )

    ecg_signal = waveforms[
        :, ecg_index
    ]

    pleth_signal = waveforms[
        :, pleth_index
    ]

    _, ecg_peaks = detect_ecg_r_peaks(
        ecg_signal,
        fs
    )

    _, pleth_peaks = detect_pleth_peaks(
        pleth_signal,
        fs
    )

    print()
    print("----------------------------------------")
    print("GLOBAL MULTIMODAL EVIDENCE")
    print("----------------------------------------")

    global_delays, _, _ = (
        calculate_ecg_pleth_delays(
            ecg_peaks,
            pleth_peaks,
            fs
        )
    )

    print(
        f"ECG R-peaks: "
        f"{len(ecg_peaks)}"
    )

    print(
        f"PLETH pulses: "
        f"{len(pleth_peaks)}"
    )

    print(
        f"Matched ECG-PLETH events: "
        f"{len(global_delays)}"
    )

    if len(global_delays) > 0:

        print(
            f"Mean ECG-PLETH delay: "
            f"{np.mean(global_delays):.3f} s"
        )

        print(
            f"Delay standard deviation: "
            f"{np.std(global_delays):.3f} s"
        )

    # --------------------------------------------------------
    # Alarm-centered evidence
    # --------------------------------------------------------

    print()
    print("----------------------------------------")
    print("ALARM-CENTERED MULTIMODAL EVIDENCE")
    print("----------------------------------------")

    alarm_analysis = analyze_alarm_window(
        ecg_peaks,
        pleth_peaks,
        alarm_sample,
        fs,
        window_seconds=5
    )

    for key, value in alarm_analysis.items():

        print(
            f"{key}: {value}"
        )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    output_path = (
        episode_path /
        "multimodal_evidence.json"
    )

    output = {

        "event": event_name,

        "sampling_frequency_hz": fs,

        "alarm_reference_sample": int(
            alarm_sample
        ),

        "global": {

            "ecg_peak_count": int(
                len(ecg_peaks)
            ),

            "pleth_peak_count": int(
                len(pleth_peaks)
            ),

            "matched_event_count": int(
                len(global_delays)
            ),

            "mean_ecg_pleth_delay_seconds":
                (
                    float(
                        np.mean(global_delays)
                    )
                    if len(global_delays) > 0
                    else None
                ),

            "std_ecg_pleth_delay_seconds":
                (
                    float(
                        np.std(global_delays)
                    )
                    if len(global_delays) > 0
                    else None
                )
        },

        "alarm_window":
            alarm_analysis
    }

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4
        )

    print()
    print("----------------------------------------")
    print("Saved to:")
    print(output_path)
    print("----------------------------------------")

    print()
    print("=" * 40)
    print("Multimodal temporal analysis complete.")
    print("=" * 40)


if __name__ == "__main__":
    main()