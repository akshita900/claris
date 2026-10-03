from pathlib import Path
import json

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch


# ============================================================
# CLARIS - Integrated Reconstructed Alarm Event Visualization
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODE_DIR = (
    PROJECT_ROOT
    / "data"
    / "episodes"
    / "003c13_0115"
)

WAVEFORM_FILE = EPISODE_DIR / "waveforms.npz"
METADATA_FILE = EPISODE_DIR / "metadata.json"
PHYSIOLOGICAL_FILE = (
    EPISODE_DIR / "physiological_features.json"
)
ALARM_CONTEXT_FILE = (
    EPISODE_DIR / "alarm_context.json"
)
ALARM_EVENT_FILE = (
    EPISODE_DIR / "alarm_event.json"
)


# ============================================================
# File loading
# ============================================================

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_episode_data():

    metadata = load_json(
        METADATA_FILE
    )

    physiological = load_json(
        PHYSIOLOGICAL_FILE
    )

    alarm_context = load_json(
        ALARM_CONTEXT_FILE
    )

    alarm_event = load_json(
        ALARM_EVENT_FILE
    )

    waveform_data = np.load(
        WAVEFORM_FILE
    )

    pre_event = waveform_data[
        "pre_event"
    ]

    post_event = waveform_data[
        "post_event"
    ]

    waveforms = np.vstack(
        (
            pre_event,
            post_event,
        )
    )

    return (
        metadata,
        physiological,
        alarm_context,
        alarm_event,
        waveforms,
    )


# ============================================================
# Metadata helpers
# ============================================================

def get_signal_names(metadata):

    return list(
        metadata[
            "signals"
        ].keys()
    )


def get_alarm_time(metadata):

    return metadata[
        "event_window"
    ][
        "alarm_reference_time_seconds"
    ]


# ============================================================
# Physiological event locations
# ============================================================

def get_peak_times(
    physiological,
    signal_name,
):
    """
    Read the already-detected event locations.

    No physiological event detection is performed here.
    """

    signal_data = physiological.get(
        signal_name
    )

    if signal_data is None:
        return np.array(
            [],
            dtype=float,
        )

    features = signal_data.get(
        "features",
        {},
    )

    peak_times = features.get(
        "peak_times_seconds",
        [],
    )

    return np.asarray(
        peak_times,
        dtype=float,
    )


# ============================================================
# ECG-PLETH matching
# ============================================================

def match_ecg_to_pleth(
    ecg_times,
    pleth_times,
    minimum_delay=0.10,
    maximum_delay=1.00,
):
    """
    Reproduce the existing CLARIS temporal matching rule.

    For each ECG event, find the next PLETH event whose
    temporal delay is between 0.10 and 1.00 seconds.

    Each PLETH event is used at most once.
    """

    matches = []

    pleth_index = 0

    for ecg_time in ecg_times:

        while (
            pleth_index < len(pleth_times)
            and pleth_times[pleth_index] <= ecg_time
        ):
            pleth_index += 1

        if pleth_index >= len(pleth_times):
            break

        candidate = pleth_times[
            pleth_index
        ]

        delay = candidate - ecg_time

        if (
            minimum_delay
            <= delay
            <= maximum_delay
        ):

            matches.append(
                {
                    "ecg_time": float(
                        ecg_time
                    ),
                    "pleth_time": float(
                        candidate
                    ),
                    "delay": float(
                        delay
                    ),
                }
            )

            pleth_index += 1

    return matches


# ============================================================
# Time axis
# ============================================================

def build_time_axis(
    start_seconds,
    end_seconds,
    sampling_frequency,
):

    start_sample = int(
        start_seconds
        * sampling_frequency
    )

    end_sample = int(
        end_seconds
        * sampling_frequency
    )

    time_axis = (
        np.arange(
            start_sample,
            end_sample,
        )
        / sampling_frequency
    )

    return (
        start_sample,
        end_sample,
        time_axis,
    )


# ============================================================
# Temporal windows
# ============================================================

def get_window_boundaries(
    alarm_time,
    windows,
):

    boundaries = []

    for name, window in windows.items():

        start_offset = window[
            "start_offset_seconds"
        ]

        end_offset = window[
            "end_offset_seconds"
        ]

        boundaries.append(
            {
                "name": name,
                "start": (
                    alarm_time
                    + start_offset
                ),
                "end": (
                    alarm_time
                    + end_offset
                ),
            }
        )

    return boundaries


# ============================================================
# Event visibility
# ============================================================

def get_visible_events(
    event_times,
    start_seconds,
    end_seconds,
):

    return event_times[
        (
            event_times
            >= start_seconds
        )
        &
        (
            event_times
            <= end_seconds
        )
    ]


# ============================================================
# Individual signal plot
# ============================================================

def plot_signal(
    signal_name,
    modality,
    signal,
    time_axis,
    alarm_time,
    boundaries,
    event_times,
):

    plt.figure(
        figsize=(14, 5)
    )

    # --------------------------------------------------------
    # Waveform
    # --------------------------------------------------------

    plt.plot(
        time_axis,
        signal,
        label=signal_name,
    )

    # --------------------------------------------------------
    # Temporal window boundaries
    # --------------------------------------------------------

    for boundary in boundaries:

        if boundary["start"] != alarm_time:

            plt.axvline(
                boundary["start"],
                linestyle=":",
                alpha=0.6,
            )

    # --------------------------------------------------------
    # Alarm reference
    # --------------------------------------------------------

    plt.axvline(
        alarm_time,
        linestyle="--",
        label="Alarm reference",
    )

    # --------------------------------------------------------
    # Detected physiological events
    # --------------------------------------------------------

    visible_events = get_visible_events(
        event_times,
        time_axis[0],
        time_axis[-1],
    )

    if len(visible_events) > 0:

        event_indices = np.searchsorted(
            time_axis,
            visible_events,
        )

        event_indices = np.clip(
            event_indices,
            0,
            len(signal) - 1,
        )

        plt.scatter(
            visible_events,
            signal[event_indices],
            marker="o",
            s=35,
            label="Detected events",
        )

    # --------------------------------------------------------
    # Temporal region labels
    # --------------------------------------------------------

    y_min = np.min(signal)
    y_max = np.max(signal)

    label_height = (
        y_max
        - 0.08 * (y_max - y_min)
    )

    for boundary in boundaries:

        midpoint = (
            boundary["start"]
            + boundary["end"]
        ) / 2

        label = boundary[
            "name"
        ].replace(
            "_",
            " ",
        )

        plt.text(
            midpoint,
            label_height,
            label,
            ha="center",
            va="top",
            fontsize=8,
        )

    # --------------------------------------------------------
    # Titles and axes
    # --------------------------------------------------------

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


# ============================================================
# Multimodal relationship visualization
# ============================================================

def plot_multimodal_relationship(
    ii_signal,
    pleth_signal,
    time_axis,
    alarm_time,
    ii_events,
    pleth_events,
    matches,
):
    """
    Visualize the measured ECG II ↔ PLETH temporal relationship.

    Each matched ECG event is explicitly connected to its
    corresponding PLETH event.

    The connector represents the measured temporal delay only.
    It is not a clinical conclusion.
    """

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(14, 8),
        sharex=True,
    )

    # ========================================================
    # ECG II
    # ========================================================

    axes[0].plot(
        time_axis,
        ii_signal,
        label="II - ECG",
    )

    visible_ii_events = get_visible_events(
        ii_events,
        time_axis[0],
        time_axis[-1],
    )

    if len(visible_ii_events) > 0:

        indices = np.searchsorted(
            time_axis,
            visible_ii_events,
        )

        indices = np.clip(
            indices,
            0,
            len(ii_signal) - 1,
        )

        axes[0].scatter(
            visible_ii_events,
            ii_signal[indices],
            marker="o",
            s=35,
            label="Detected ECG events",
        )

    axes[0].axvline(
        alarm_time,
        linestyle="--",
        label="Alarm reference",
    )

    axes[0].set_ylabel(
        "ECG amplitude"
    )

    axes[0].set_title(
        "CLARIS Multimodal Evidence - ECG II ↔ PLETH"
    )

    axes[0].legend()

    # ========================================================
    # PLETH
    # ========================================================

    axes[1].plot(
        time_axis,
        pleth_signal,
        label="PLETH - PPG",
    )

    visible_pleth_events = get_visible_events(
        pleth_events,
        time_axis[0],
        time_axis[-1],
    )

    if len(visible_pleth_events) > 0:

        indices = np.searchsorted(
            time_axis,
            visible_pleth_events,
        )

        indices = np.clip(
            indices,
            0,
            len(pleth_signal) - 1,
        )

        axes[1].scatter(
            visible_pleth_events,
            pleth_signal[indices],
            marker="o",
            s=35,
            label="Detected PLETH events",
        )

    axes[1].axvline(
        alarm_time,
        linestyle="--",
        label="Alarm reference",
    )

    axes[1].set_xlabel(
        "Time (seconds)"
    )

    axes[1].set_ylabel(
        "PPG amplitude"
    )

    axes[1].legend()

    # ========================================================
    # Explicit ECG → PLETH matched-event connections
    # ========================================================

    visible_matches = []

    for match in matches:

        if (
            match["ecg_time"] >= time_axis[0]
            and
            match["ecg_time"] <= time_axis[-1]
        ):
            visible_matches.append(
                match
            )

    for match in visible_matches:

        ecg_time = match[
            "ecg_time"
        ]

        pleth_time = match[
            "pleth_time"
        ]

        # ----------------------------------------------------
        # Find waveform amplitudes at the matched event times
        # ----------------------------------------------------

        ecg_amplitude = np.interp(
            ecg_time,
            time_axis,
            ii_signal,
        )

        pleth_amplitude = np.interp(
            pleth_time,
            time_axis,
            pleth_signal,
        )

        # ----------------------------------------------------
        # Connect ECG event to corresponding PLETH event
        # ----------------------------------------------------

        connector = ConnectionPatch(
            xyA=(
                ecg_time,
                ecg_amplitude,
            ),
            xyB=(
                pleth_time,
                pleth_amplitude,
            ),
            coordsA="data",
            coordsB="data",
            axesA=axes[0],
            axesB=axes[1],
            linestyle=":",
            alpha=0.45,
        )

        fig.add_artist(
            connector
        )

    # ========================================================
    # Figure title
    # ========================================================

    fig.suptitle(
        "Measured ECG II - PLETH Temporal Relationship",
        fontsize=14,
    )

    plt.tight_layout()

    plt.show()

    # ========================================================
    # Terminal matching information
    # ========================================================

    print(
        "\nECG II ↔ PLETH matches "
        "visible in ±10 s window:"
    )

    for match in visible_matches:

        print(
            f"  ECG: "
            f"{match['ecg_time']:.3f} s"
            f"  ->  "
            f"PLETH: "
            f"{match['pleth_time']:.3f} s"
            f"  | delay: "
            f"{match['delay']:.3f} s"
        )

    print(
        f"\nVisible matched events: "
        f"{len(visible_matches)}"
    )


# ============================================================
# Terminal reconstruction summary
# ============================================================

def print_reconstruction_summary(
    alarm_event,
    physiological,
):

    print(
        "\n========================================"
    )

    print(
        "CLARIS - Integrated Alarm Reconstruction"
    )

    print(
        "========================================"
    )

    print(
        f"Episode: "
        f"{alarm_event['episode']}"
    )

    event_metadata = alarm_event[
        "event_metadata"
    ]

    print(
        f"Alarm reference: "
        f"{event_metadata['alarm_reference_time_seconds']:.3f} s"
    )

    print(
        f"Sampling frequency: "
        f"{event_metadata['sampling_frequency_hz']} Hz"
    )

    print(
        "\nDetected physiological events:"
    )

    for signal_name in [
        "II",
        "aVR",
        "V",
        "PLETH",
    ]:

        signal_data = physiological.get(
            signal_name
        )

        if signal_data is None:
            continue

        features = signal_data[
            "features"
        ]

        print(
            f"  {signal_name}: "
            f"{features['peak_count']} global, "
            f"{features['local_peak_count']} local"
        )

    # --------------------------------------------------------
    # Existing alarm-window multimodal evidence
    # --------------------------------------------------------

    print(
        "\nExisting alarm-window multimodal evidence:"
    )

    multimodal = alarm_event[
        "multimodal_evidence"
    ]

    alarm_window = multimodal[
        "alarm_window_observation"
    ]

    print(
        f"  ECG events: "
        f"{alarm_window['ecg_events']}"
    )

    print(
        f"  Matched events: "
        f"{alarm_window['matched_events']}"
    )

    print(
        f"  Matching fraction: "
        f"{alarm_window['matching_fraction']:.3f}"
    )

    print(
        f"  Mean delay: "
        f"{alarm_window['mean_delay_seconds']:.4f} s"
    )

    # --------------------------------------------------------
    # Clinical boundary
    # --------------------------------------------------------

    print(
        "\nClinical boundary:"
    )

    boundary = alarm_event[
        "clinical_boundary"
    ]

    print(
        f"  Credibility score: "
        f"{boundary['credibility_score']}"
    )

    print(
        f"  Credibility status: "
        f"{boundary['credibility_status']}"
    )

    print(
        f"  Clinical decision: "
        f"{boundary['clinical_decision']}"
    )


# ============================================================
# Main
# ============================================================

def main():

    (
        metadata,
        physiological,
        alarm_context,
        alarm_event,
        waveforms,
    ) = load_episode_data()

    sampling_frequency = metadata[
        "sampling_frequency_hz"
    ]

    alarm_time = get_alarm_time(
        metadata
    )

    # --------------------------------------------------------
    # ±10 second alarm-centered window
    # --------------------------------------------------------

    start_seconds = (
        alarm_time - 10
    )

    end_seconds = (
        alarm_time + 10
    )

    (
        start_sample,
        end_sample,
        time_axis,
    ) = build_time_axis(
        start_seconds,
        end_seconds,
        sampling_frequency,
    )

    segment = waveforms[
        start_sample:end_sample
    ]

    # --------------------------------------------------------
    # Temporal context
    # --------------------------------------------------------

    windows = alarm_context[
        "windows"
    ]

    boundaries = get_window_boundaries(
        alarm_time,
        windows,
    )

    # --------------------------------------------------------
    # Load actual detected event locations
    # --------------------------------------------------------

    ii_events = get_peak_times(
        physiological,
        "II",
    )

    avr_events = get_peak_times(
        physiological,
        "aVR",
    )

    v_events = get_peak_times(
        physiological,
        "V",
    )

    pleth_events = get_peak_times(
        physiological,
        "PLETH",
    )

    # --------------------------------------------------------
    # Reproduce existing ECG II ↔ PLETH matching rule
    # for visualization only
    # --------------------------------------------------------

    matches = match_ecg_to_pleth(
        ii_events,
        pleth_events,
    )

    # --------------------------------------------------------
    # Terminal summary
    # --------------------------------------------------------

    print_reconstruction_summary(
        alarm_event,
        physiological,
    )

    print(
        f"\nLoaded ECG II events: "
        f"{len(ii_events)}"
    )

    print(
        f"Loaded PLETH events: "
        f"{len(pleth_events)}"
    )

    print(
        f"Reconstructed ECG II ↔ PLETH matches: "
        f"{len(matches)}"
    )

    # --------------------------------------------------------
    # Individual signal plots
    # --------------------------------------------------------

    signal_names = get_signal_names(
        metadata
    )

    event_map = {
        "II": ii_events,
        "aVR": avr_events,
        "V": v_events,
        "PLETH": pleth_events,
    }

    for index, signal_name in enumerate(
        signal_names
    ):

        modality = metadata[
            "signals"
        ][
            signal_name
        ][
            "modality"
        ]

        plot_signal(
            signal_name,
            modality,
            segment[:, index],
            time_axis,
            alarm_time,
            boundaries,
            event_map.get(
                signal_name,
                np.array([]),
            ),
        )

    # --------------------------------------------------------
    # Dedicated multimodal plot
    # --------------------------------------------------------

    if (
        "II" in signal_names
        and
        "PLETH" in signal_names
    ):

        ii_index = signal_names.index(
            "II"
        )

        pleth_index = signal_names.index(
            "PLETH"
        )

        plot_multimodal_relationship(
            segment[:, ii_index],
            segment[:, pleth_index],
            time_axis,
            alarm_time,
            ii_events,
            pleth_events,
            matches,
        )


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()