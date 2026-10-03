from pathlib import Path
import json

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# CLARIS - Episode Visualization
# Phase 2.4
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODE_DIR = PROJECT_ROOT / "data" / "episodes"


def load_episode(event_name):
    """
    Load a reconstructed CLARIS episode.
    """

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


def plot_alarm_window(
    metadata,
    waveforms,
    start_seconds=295,
    end_seconds=305,
):
    """
    Plot all available signals around the alarm reference.

    Default window:
        5 seconds before alarm
        to
        5 seconds after alarm
    """

    fs = metadata["sampling_frequency_hz"]

    alarm_time = metadata[
        "event_window"
    ][
        "alarm_reference_time_seconds"
    ]

    signal_names = list(
        metadata["signals"].keys()
    )

    start_sample = int(start_seconds * fs)
    end_sample = int(end_seconds * fs)

    segment = waveforms[
        start_sample:end_sample
    ]

    time_axis = (
        np.arange(
            start_sample,
            end_sample
        ) / fs
    )

    # --------------------------------------------------------
    # Create one plot per signal
    # --------------------------------------------------------

    for index, signal_name in enumerate(signal_names):

        plt.figure(
            figsize=(12, 4)
        )

        plt.plot(
            time_axis,
            segment[:, index]
        )

        plt.axvline(
            alarm_time,
            linestyle="--",
            label="Alarm reference"
        )

        modality = metadata[
            "signals"
        ][
            signal_name
        ][
            "modality"
        ]

        plt.title(
            f"{signal_name} - {modality}"
        )

        plt.xlabel(
            "Time (seconds)"
        )

        plt.ylabel(
            "Amplitude"
        )

        plt.legend()

        plt.tight_layout()

        plt.show()


def main():

    # First CLARIS episode
    event_name = "003c13_0115"

    # Load reconstructed episode
    metadata, waveforms = load_episode(
        event_name
    )

    print("\n========================================")
    print("CLARIS - Episode Visualization")
    print("========================================")

    print(
        f"Event: {event_name}"
    )

    print(
        "\nPlotting 5 seconds before "
        "and 5 seconds after the alarm."
    )

    print(
        "Close each plot window to continue."
    )

    # Plot the alarm-centered region
    plot_alarm_window(
        metadata,
        waveforms,
        start_seconds=295,
        end_seconds=305,
    )


if __name__ == "__main__":
    main()