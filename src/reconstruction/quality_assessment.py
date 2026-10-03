from pathlib import Path
import json
import sys

import numpy as np


# ============================================================
# CLARIS - Signal Quality Assessment
# Phase 2.3
# ============================================================


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJECT_ROOT / "src"
EPISODE_DIR = PROJECT_ROOT / "data" / "episodes"


# ------------------------------------------------------------
# Make src/ available for imports
# ------------------------------------------------------------

sys.path.insert(0, str(SRC_DIR))

from signal_quality import calculate_signal_quality_features


# ============================================================
# Load reconstructed episode
# ============================================================

def load_episode(event_name):
    """
    Load a reconstructed CLARIS episode.

    Returns
    -------
    metadata : dict
        Episode metadata.

    waveforms : np.ndarray
        Complete reconstructed waveform matrix.
    """

    episode_path = EPISODE_DIR / event_name

    metadata_path = episode_path / "metadata.json"
    waveform_path = episode_path / "waveforms.npz"

    # Load metadata
    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    # Load waveform arrays
    waveform_data = np.load(waveform_path)

    pre_event = waveform_data["pre_event"]
    post_event = waveform_data["post_event"]

    # Reconstruct the complete six-minute recording
    waveforms = np.vstack(
        (pre_event, post_event)
    )

    return metadata, waveforms


# ============================================================
# Assess signal quality
# ============================================================

def assess_signal_quality(metadata, waveforms):
    """
    Calculate measurable signal-quality features
    for every available physiological channel.

    No clinical quality label is assigned here.
    """

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

    quality_results = {}

    for index, signal_name in enumerate(signal_names):

        # Extract one channel
        signal = waveforms[:, index]

        # Calculate measurable features
        features = calculate_signal_quality_features(
            signal=signal,
            sampling_frequency=sampling_frequency,
            alarm_sample=alarm_sample,
            window_seconds=1.0,
        )

        quality_results[signal_name] = {
            "modality":
                metadata["signals"][signal_name]["modality"],

            "features":
                features,
        }

    return quality_results


# ============================================================
# Save quality results
# ============================================================

def save_quality_results(
    event_name,
    quality_results
):
    """
    Save signal-quality measurements separately
    from the original waveform data.
    """

    episode_path = EPISODE_DIR / event_name

    output_path = (
        episode_path /
        "signal_quality.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            quality_results,
            file,
            indent=4
        )

    return output_path


# ============================================================
# Print quality summary
# ============================================================

def print_quality_summary(
    quality_results,
    output_path
):
    """
    Display measurable signal-quality features.
    """

    print("\n========================================")
    print("CLARIS - Signal Quality Assessment")
    print("========================================")

    for signal_name, result in quality_results.items():

        print(f"\nSignal: {signal_name}")

        print(
            f"Modality: "
            f"{result['modality']}"
        )

        features = result["features"]

        print(
            f"  NaN count: "
            f"{features['nan_count']}"
        )

        print(
            f"  Inf count: "
            f"{features['inf_count']}"
        )

        print(
            f"  Repeat fraction: "
            f"{features['repeat_fraction']:.6f}"
        )

        print(
            f"  Longest repeated run: "
            f"{features['longest_repeat_samples']} "
            f"samples"
        )

        print(
            f"  Longest repeated duration: "
            f"{features['longest_repeat_duration']:.6f} s"
        )

        print(
            f"  Local mean: "
            f"{features['local_mean']:.6f}"
        )

        print(
            f"  Local standard deviation: "
            f"{features['local_std']:.6f}"
        )

        print(
            f"  Local range: "
            f"{features['local_range']:.6f}"
        )

        print(
            f"  Minimum count: "
            f"{features['minimum_count']}"
        )

        print(
            f"  Maximum count: "
            f"{features['maximum_count']}"
        )

    print("\n----------------------------------------")
    print("Saved to:")
    print(output_path)

    print("\n========================================")
    print("Signal-quality assessment complete.")
    print("========================================")


# ============================================================
# Main
# ============================================================

def main():

    # First real CLARIS episode
    event_name = "003c13_0115"

    # Load reconstructed episode
    metadata, waveforms = load_episode(
        event_name
    )

    # Calculate quality features
    quality_results = assess_signal_quality(
        metadata,
        waveforms
    )

    # Save results
    output_path = save_quality_results(
        event_name,
        quality_results
    )

    # Display results
    print_quality_summary(
        quality_results,
        output_path
    )


if __name__ == "__main__":
    main()