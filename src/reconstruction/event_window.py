from pathlib import Path
import json

import numpy as np
import pandas as pd
import wfdb


# ============================================================
# CLARIS - Event-Centered Waveform Reconstruction
# Phase 2.1
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "Vtac"
EPISODE_DIR = PROJECT_ROOT / "data" / "episodes"

LABEL_FILE = RAW_DATA_DIR / "event_labels.csv"


def load_event(event_name):
    """
    Load one VTaC waveform event and its metadata.
    """

    record_path = RAW_DATA_DIR / event_name

    record = wfdb.rdrecord(str(record_path))

    return {
        "event": event_name,
        "signals": record.p_signal,
        "signal_names": record.sig_name,
        "sampling_frequency": record.fs,
        "number_of_samples": record.sig_len,
        "number_of_channels": record.n_sig,
    }


def load_event_label(event_name):
    """
    Load the human annotation associated with the event.

    The annotation is kept separate from the physiological
    waveform evidence used by CLARIS.
    """

    if not LABEL_FILE.exists():
        return None

    labels = pd.read_csv(LABEL_FILE)

    matching_rows = labels[labels["event"] == event_name]

    if matching_rows.empty:
        return None

    row = matching_rows.iloc[0]

    return {
        "record": row["record"],
        "event": row["event"],
        "decision": bool(row["decision"]),
    }


def reconstruct_event(event):
    """
    Create the event-centered temporal structure.

    VTaC recordings contain:
        5 minutes before the alarm
        1 minute after the alarm

    The alarm reference is therefore at 300 seconds.
    """

    fs = event["sampling_frequency"]

    pre_event_seconds = 5 * 60
    post_event_seconds = 1 * 60

    alarm_sample = int(pre_event_seconds * fs)

    pre_event = event["signals"][:alarm_sample]
    post_event = event["signals"][alarm_sample:]

    return {
        "event": event["event"],
        "sampling_frequency": fs,
        "signal_names": event["signal_names"],
        "total_samples": event["number_of_samples"],
        "number_of_channels": event["number_of_channels"],
        "alarm_reference_sample": alarm_sample,
        "alarm_reference_time_seconds": pre_event_seconds,
        "pre_event": pre_event,
        "post_event": post_event,
        "pre_event_duration_seconds": pre_event_seconds,
        "post_event_duration_seconds": post_event_seconds,
    }


def classify_signal(signal_name):
    """
    Assign a broad physiological category to a waveform channel.
    """

    name = signal_name.upper()

    if name in {"II", "III", "I", "AVR", "AVL", "AVF", "V"}:
        return "ECG"

    if name in {"PLETH", "PPG"}:
        return "PPG"

    if name in {"ABP", "ART"}:
        return "ABP"

    if name in {"RESP", "RESPIRATION"}:
        return "RESP"

    return "UNKNOWN"


def build_signal_metadata(signal_names):
    """
    Create metadata describing the available physiological modalities.
    """

    signal_metadata = {}

    for signal_name in signal_names:
        signal_metadata[signal_name] = {
            "modality": classify_signal(signal_name)
        }

    return signal_metadata


def save_reconstructed_episode(reconstructed_event, annotation):
    """
    Save the reconstructed episode to data/episodes/.
    """

    event_name = reconstructed_event["event"]

    output_dir = EPISODE_DIR / event_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Save waveform arrays
    # --------------------------------------------------------

    waveform_path = output_dir / "waveforms.npz"

    np.savez_compressed(
        waveform_path,
        pre_event=reconstructed_event["pre_event"],
        post_event=reconstructed_event["post_event"],
    )

    # --------------------------------------------------------
    # Build metadata
    # --------------------------------------------------------

    signal_metadata = build_signal_metadata(
        reconstructed_event["signal_names"]
    )

    metadata = {
        "event": event_name,

        "sampling_frequency_hz":
            reconstructed_event["sampling_frequency"],

        "total_samples":
            reconstructed_event["total_samples"],

        "number_of_channels":
            reconstructed_event["number_of_channels"],

        "signals":
            signal_metadata,

        "event_window": {
            "total_duration_seconds": 360,
            "pre_event_duration_seconds":
                reconstructed_event["pre_event_duration_seconds"],
            "post_event_duration_seconds":
                reconstructed_event["post_event_duration_seconds"],
            "alarm_reference_time_seconds":
                reconstructed_event["alarm_reference_time_seconds"],
            "alarm_reference_sample":
                reconstructed_event["alarm_reference_sample"],
        },

        "annotation": annotation,
    }

    metadata_path = output_dir / "metadata.json"

    with open(metadata_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)

    return output_dir


def print_summary(reconstructed_event, annotation, output_dir):
    """
    Print a readable reconstruction summary.
    """

    print("\n========================================")
    print("CLARIS - Episode Reconstruction")
    print("========================================")

    print(f"Event: {reconstructed_event['event']}")

    print(
        f"Sampling frequency: "
        f"{reconstructed_event['sampling_frequency']} Hz"
    )

    print(
        f"Channels: "
        f"{reconstructed_event['number_of_channels']}"
    )

    print(
        f"Total samples: "
        f"{reconstructed_event['total_samples']}"
    )

    print("\nSignals:")

    for signal_name in reconstructed_event["signal_names"]:
        modality = classify_signal(signal_name)

        print(f"  {signal_name} -> {modality}")

    print("\n----------------------------------------")
    print("EVENT WINDOW")
    print("----------------------------------------")

    print("Pre-event: 0 - 300 seconds")
    print("Alarm reference: 300 seconds")
    print("Post-event: 300 - 360 seconds")

    print(
        f"\nAlarm reference sample: "
        f"{reconstructed_event['alarm_reference_sample']}"
    )

    print(
        f"Pre-event samples: "
        f"{len(reconstructed_event['pre_event'])}"
    )

    print(
        f"Post-event samples: "
        f"{len(reconstructed_event['post_event'])}"
    )

    print("\n----------------------------------------")
    print("DATASET ANNOTATION")
    print("----------------------------------------")

    if annotation is not None:
        print(f"Decision: {annotation['decision']}")
    else:
        print("No annotation found.")

    print("\n----------------------------------------")
    print("SAVED EPISODE")
    print("----------------------------------------")

    print(output_dir)

    print("\n========================================")
    print("Reconstruction saved successfully.")
    print("========================================")


def main():

    # First real CLARIS episode
    event_name = "003c13_0115"

    # Load raw waveform
    event = load_event(event_name)

    # Load dataset annotation separately
    annotation = load_event_label(event_name)

    # Reconstruct the event-centered window
    reconstructed_event = reconstruct_event(event)

    # Save reconstructed episode
    output_dir = save_reconstructed_episode(
        reconstructed_event,
        annotation
    )

    # Display summary
    print_summary(
        reconstructed_event,
        annotation,
        output_dir
    )


if __name__ == "__main__":
    main()