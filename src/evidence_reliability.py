
import json
from pathlib import Path
from datetime import datetime, timezone


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

EPISODE_DIR = (
    BASE_DIR
    / "data"
    / "episodes"
    / "003c13_0115"
)

SIGNAL_QUALITY_FILE = EPISODE_DIR / "signal_quality.json"
PHYSIOLOGICAL_FILE = EPISODE_DIR / "physiological_features.json"
MULTIMODAL_FILE = EPISODE_DIR / "multimodal_evidence.json"

OUTPUT_FILE = EPISODE_DIR / "evidence_reliability.json"


# ============================================================
# JSON UTILITIES
# ============================================================

def load_json(path):

    if not path.exists():
        raise FileNotFoundError(
            f"Required input file not found: {path}"
        )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_channel_records(data, known_channels):

    records = {}

    def traverse(node):

        if isinstance(node, dict):

            for key, value in node.items():

                if (
                    key in known_channels
                    and isinstance(value, dict)
                ):
                    records[key] = value

                traverse(value)

        elif isinstance(node, list):

            for item in node:
                traverse(item)

    traverse(data)

    return records


def collect_values(data, candidate_keys):

    results = {}

    def traverse(node):

        if isinstance(node, dict):

            for key, value in node.items():

                if key in candidate_keys:
                    results[key] = value

                traverse(value)

        elif isinstance(node, list):

            for item in node:
                traverse(item)

    traverse(data)

    return results


# ============================================================
# SIGNAL QUALITY ASSESSMENT
# ============================================================

def assess_signal_quality(signal_quality):

    known_channels = ["II", "aVR", "V", "PLETH"]

    channel_records = find_channel_records(
        signal_quality,
        known_channels
    )

    results = {}
    limitations = []

    for channel in known_channels:

        record = channel_records.get(channel)

        if record is None:

            results[channel] = {
                "available": False,
                "assessment": "signal_quality_record_missing"
            }

            limitations.append(
                f"Signal-quality record unavailable for {channel}."
            )

            continue

        features = record.get("features", record)

        if not isinstance(features, dict):
            features = {}

        results[channel] = {
            "available": True,
            "modality": record.get("modality"),

            "nan_count": features.get("nan_count"),
            "inf_count": features.get("inf_count"),

            "repeat_fraction": features.get(
                "repeat_fraction"
            ),

            "longest_repeat_samples": features.get(
                "longest_repeat_samples"
            ),

            "longest_repeat_seconds": features.get(
                "longest_repeat_duration"
            ),

            "local_mean": features.get("local_mean"),
            "local_std": features.get("local_std"),

            "signal_range": features.get("local_range"),

            "minimum_count": features.get("minimum_count"),
            "maximum_count": features.get("maximum_count")
        }

        if (
            features.get("nan_count") is None
            or features.get("inf_count") is None
        ):

            limitations.append(
                f"Non-finite value counts are incomplete for {channel}."
            )

        repeat_fraction = features.get("repeat_fraction")

        if (
            isinstance(repeat_fraction, (int, float))
            and repeat_fraction > 0
        ):

            limitations.append(
                f"{channel} contains repeated-value samples; "
                "their effect on waveform interpretation requires "
                "contextual review."
            )

    return results, limitations


# ============================================================
# PHYSIOLOGICAL FEATURE EXTRACTION
# ============================================================

PHYSIOLOGICAL_KEYS = {
    "peak_count",
    "local_peak_count",
    "mean_rr_seconds",
    "std_rr_seconds",
    "mean_heart_rate_bpm",
    "mean_pulse_interval_seconds",
    "mean_pulse_rate_bpm",
    "filtered_signal_std",
    "peak_times_seconds",
    "rr_intervals_seconds",
    "pulse_intervals_seconds"
}


def assess_physiological_evidence(physiological):

    known_channels = ["II", "aVR", "V", "PLETH"]

    channel_records = find_channel_records(
        physiological,
        known_channels
    )

    results = {}
    limitations = []

    for channel in known_channels:

        record = channel_records.get(channel)

        if record is None:

            results[channel] = {
                "available": False,
                "assessment": "physiological_record_missing"
            }

            limitations.append(
                f"Physiological evidence unavailable for {channel}."
            )

            continue

        values = collect_values(
            record,
            PHYSIOLOGICAL_KEYS
        )

        peak_times = values.get("peak_times_seconds")

        if isinstance(peak_times, list):
            detected_peak_time_count = len(peak_times)
        else:
            detected_peak_time_count = None

        results[channel] = {
            "available": True,

            "peak_count": values.get("peak_count"),
            "local_peak_count": values.get("local_peak_count"),

            "detected_peak_time_count": detected_peak_time_count,

            "mean_rr_seconds": values.get("mean_rr_seconds"),
            "std_rr_seconds": values.get("std_rr_seconds"),

            "mean_heart_rate_bpm": values.get(
                "mean_heart_rate_bpm"
            ),

            "mean_pulse_interval_seconds": values.get(
                "mean_pulse_interval_seconds"
            ),

            "mean_pulse_rate_bpm": values.get(
                "mean_pulse_rate_bpm"
            ),

            "filtered_signal_std": values.get(
                "filtered_signal_std"
            )
        }

        if (
            channel != "PLETH"
            and values.get("mean_heart_rate_bpm") is None
        ):

            limitations.append(
                f"Heart-rate estimate unavailable for {channel}."
            )

        if (
            channel == "PLETH"
            and values.get("mean_pulse_rate_bpm") is None
        ):

            limitations.append(
                "Pulse-rate estimate unavailable for PLETH."
            )

    return results, limitations


# ============================================================
# MULTIMODAL EVIDENCE
# ============================================================

def assess_multimodal_evidence(multimodal):

    global_data = multimodal.get("global", {})
    alarm_data = multimodal.get("alarm_window", {})

    results = {

        "global": {
            "ecg_peak_count": global_data.get(
                "ecg_peak_count"
            ),

            "pleth_peak_count": global_data.get(
                "pleth_peak_count"
            ),

            "matched_event_count": global_data.get(
                "matched_event_count"
            ),

            "mean_ecg_pleth_delay_seconds": global_data.get(
                "mean_ecg_pleth_delay_seconds"
            ),

            "std_ecg_pleth_delay_seconds": global_data.get(
                "std_ecg_pleth_delay_seconds"
            )
        },

        "alarm_window": {
            "window_seconds": alarm_data.get(
                "window_seconds"
            ),

            "ecg_peak_count": alarm_data.get(
                "ecg_peak_count"
            ),

            "pleth_peak_count": alarm_data.get(
                "pleth_peak_count"
            ),

            "matched_beat_count": alarm_data.get(
                "matched_beat_count"
            ),

            "matching_fraction": alarm_data.get(
                "matching_fraction"
            ),

            "ecg_pleth_delay_mean_seconds": alarm_data.get(
                "ecg_pleth_delay_mean_seconds"
            ),

            "ecg_pleth_delay_std_seconds": alarm_data.get(
                "ecg_pleth_delay_std_seconds"
            ),

            "ecg_pleth_delay_min_seconds": alarm_data.get(
                "ecg_pleth_delay_min_seconds"
            ),

            "ecg_pleth_delay_max_seconds": alarm_data.get(
                "ecg_pleth_delay_max_seconds"
            )
        }
    }

    limitations = [

        "ECG-PLETH matching fraction describes detected event "
        "correspondence, not alarm credibility.",

        "Matched events depend on the selected detection "
        "and temporal matching parameters.",

        "ECG-PLETH delay represents temporal association and "
        "does not establish causation or clinical validity."
    ]

    return results, limitations


# ============================================================
# RELIABILITY EVIDENCE CONSOLIDATION
# ============================================================

def build_reliability_profile():

    signal_quality = load_json(SIGNAL_QUALITY_FILE)
    physiological = load_json(PHYSIOLOGICAL_FILE)
    multimodal = load_json(MULTIMODAL_FILE)

    quality_results, quality_limitations = (
        assess_signal_quality(signal_quality)
    )

    physiological_results, physiological_limitations = (
        assess_physiological_evidence(physiological)
    )

    multimodal_results, multimodal_limitations = (
        assess_multimodal_evidence(multimodal)
    )

    limitations = (
        quality_limitations
        + physiological_limitations
        + multimodal_limitations
    )

    limitations.extend([

        "Signal-quality measurements are descriptive and do not "
        "constitute clinical signal-quality validation.",

        "Detected peaks and derived physiological features may "
        "contain detection errors.",

        "The available evidence does not establish whether the "
        "alarm represents a true or false clinical event.",

        "No alarm credibility score is assigned.",

        "No clinical decision is generated."
    ])

    profile = {

        "project": "CLARIS",

        "module": "Evidence Reliability Assessment",

        "event": multimodal.get("event"),

        "sampling_frequency_hz": multimodal.get(
            "sampling_frequency_hz"
        ),

        "alarm_reference_sample": multimodal.get(
            "alarm_reference_sample"
        ),

        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),

        "assessment_scope": {

            "signal_quality": True,

            "physiological_measurements": True,

            "multimodal_correspondence": True,

            "clinical_alarm_validity": False
        },

        "signal_quality_evidence": quality_results,

        "physiological_evidence": physiological_results,

        "multimodal_evidence": multimodal_results,

        "reliability_interpretation": {

            "status": "descriptive_evidence_only",

            "available_evidence": [

                "Signal-quality measurements",

                "Detected physiological events",

                "ECG-PLETH temporal correspondence"
            ],

            "unresolved_questions": [

                "Clinical validity of detected events",

                "Effect of signal artifacts on event detection",

                "Clinical interpretation of alarm context"
            ],

            "alarm_credibility_score": None,

            "clinical_decision": None
        },

        "limitations": list(dict.fromkeys(limitations))
    }

    return profile


# ============================================================
# MAIN
# ============================================================

def main():

    profile = build_reliability_profile()

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            profile,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nCLARIS - Evidence Reliability Assessment")
    print("=" * 50)

    print(f"Event: {profile['event']}")

    print(
        "Signal-quality channels:",
        len(profile["signal_quality_evidence"])
    )

    print(
        "Physiological channels:",
        len(profile["physiological_evidence"])
    )

    print(
        "Limitations recorded:",
        len(profile["limitations"])
    )

    print(
        "Assessment status:",
        profile["reliability_interpretation"]["status"]
    )

    print(
        "Alarm credibility score:",
        profile["reliability_interpretation"][
            "alarm_credibility_score"
        ]
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
