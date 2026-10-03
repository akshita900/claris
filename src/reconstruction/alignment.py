from pathlib import Path
import json

import numpy as np


# ============================================================
# CLARIS - Multimodal Temporal Alignment
# Phase 2.2
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODE_DIR = PROJECT_ROOT / "data" / "episodes"


def load_episode(event_name):
    """
    Load a reconstructed CLARIS episode.

    Returns
    -------
    metadata : dict
        Episode metadata.

    waveforms : dict
        Reconstructed waveform arrays.
    """

    episode_path = EPISODE_DIR / event_name

    metadata_path = episode_path / "metadata.json"
    waveform_path = episode_path / "waveforms.npz"

    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    waveform_data = np.load(waveform_path)

    waveforms = {
        "pre_event": waveform_data["pre_event"],
        "post_event": waveform_data["post_event"],
    }

    return metadata, waveforms


def create_time_axis(number_of_samples, sampling_frequency):
    """
    Create a time axis corresponding to the waveform samples.

    Example:
        250 Hz -> 0.004 seconds per sample
    """

    return np.arange(number_of_samples) / sampling_frequency


def create_aligned_episode(metadata, waveforms):
    """
    Create one common temporal representation for all available signals.
    """

    fs = metadata["sampling_frequency_hz"]

    pre_event = waveforms["pre_event"]
    post_event = waveforms["post_event"]

    # Reconstruct the complete six-minute waveform.
    full_waveform = np.vstack((pre_event, post_event))

    number_of_samples = full_waveform.shape[0]

    # Create a common time axis.
    time_axis = create_time_axis(
        number_of_samples,
        fs
    )

    # Alarm reference is at 300 seconds.
    alarm_reference_time = (
        metadata["event_window"]["alarm_reference_time_seconds"]
    )

    alarm_reference_sample = (
        metadata["event_window"]["alarm_reference_sample"]
    )

    return {
        "waveforms": full_waveform,
        "time_axis": time_axis,
        "sampling_frequency": fs,
        "signal_names": list(metadata["signals"].keys()),
        "alarm_reference_time": alarm_reference_time,
        "alarm_reference_sample": alarm_reference_sample,
    }


def verify_alignment(aligned_episode):
    """
    Verify that all signals share the same temporal structure.
    """

    waveforms = aligned_episode["waveforms"]
    time_axis = aligned_episode["time_axis"]

    number_of_samples = waveforms.shape[0]

    checks = {
        "waveform_samples_match_time_axis":
            number_of_samples == len(time_axis),

        "alarm_reference_within_recording":
            (
                0
                <= aligned_episode["alarm_reference_sample"]
                < number_of_samples
            ),

        "sampling_frequency_valid":
            aligned_episode["sampling_frequency"] > 0,
    }

    return checks


def print_alignment_summary(metadata, aligned_episode, checks):
    """
    Print the alignment results.
    """

    print("\n========================================")
    print("CLARIS - Multimodal Temporal Alignment")
    print("========================================")

    print(f"Event: {metadata['event']}")

    print(
        f"Sampling frequency: "
        f"{aligned_episode['sampling_frequency']} Hz"
    )

    print(
        f"Number of samples: "
        f"{len(aligned_episode['time_axis'])}"
    )

    print(
        f"Duration: "
        f"{aligned_episode['time_axis'][-1]:.3f} seconds"
    )

    print("\nSignals:")

    for signal_name in aligned_episode["signal_names"]:
        modality = metadata["signals"][signal_name]["modality"]
        print(f"  {signal_name} -> {modality}")

    print("\n----------------------------------------")
    print("COMMON TIME REFERENCE")
    print("----------------------------------------")

    print(
        f"Alarm reference time: "
        f"{aligned_episode['alarm_reference_time']:.3f} seconds"
    )

    print(
        f"Alarm reference sample: "
        f"{aligned_episode['alarm_reference_sample']}"
    )

    print("\n----------------------------------------")
    print("ALIGNMENT CHECKS")
    print("----------------------------------------")

    for check_name, result in checks.items():

        status = "PASS" if result else "FAIL"

        print(
            f"{status}: {check_name}"
        )

    print("\n========================================")

    if all(checks.values()):
        print("Multimodal alignment verified.")
    else:
        print("Alignment verification failed.")

    print("========================================")


def main():

    # First reconstructed CLARIS episode
    event_name = "003c13_0115"

    # Load reconstructed episode
    metadata, waveforms = load_episode(event_name)

    # Create common temporal representation
    aligned_episode = create_aligned_episode(
        metadata,
        waveforms
    )

    # Verify temporal alignment
    checks = verify_alignment(
        aligned_episode
    )

    # Display results
    print_alignment_summary(
        metadata,
        aligned_episode,
        checks
    )


if __name__ == "__main__":
    main()