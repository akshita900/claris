from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EPISODE_DIR = PROJECT_ROOT / "data" / "episodes"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def assess_signal_quality(signal_quality):
    """
    Convert measured signal-quality features into
    transparent evidence observations.

    No clinical interpretation or credibility score
    is assigned here.
    """

    assessment = {}

    for signal_name, result in signal_quality.items():

        features = result.get("features", {})

        observations = []

        if features.get("nan_count", 0) > 0:
            observations.append(
                "NaN samples are present."
            )

        if features.get("inf_count", 0) > 0:
            observations.append(
                "Infinite samples are present."
            )

        if features.get("repeat_fraction", 0) > 0:
            observations.append(
                "Repeated-value samples are present."
            )

        if not observations:
            observations.append(
                "No missing, infinite, or repeated-value "
                "issue was detected by the available "
                "quality features."
            )

        assessment[signal_name] = {
            "evidence_type": "signal_quality",
            "observations": observations,
            "features_available": True
        }

    return assessment


def assess_physiology(physiological):
    """
    Summarize measurable physiological-event evidence.

    These observations describe detected events only.
    They do not represent a diagnosis or clinical judgment.
    """

    assessment = {}

    for signal_name, result in physiological.items():

        features = result.get("features", {})

        observations = []

        peak_count = features.get("peak_count")
        local_peak_count = features.get("local_peak_count")

        if peak_count is not None:
            observations.append(
                f"{peak_count} events were detected "
                "across the recording."
            )

        if local_peak_count is not None:
            observations.append(
                f"{local_peak_count} events were detected "
                "within the local alarm window."
            )

        if features.get("mean_heart_rate_bpm") is not None:
            observations.append(
                "A recording-level heart-rate estimate "
                "is available."
            )

        if features.get("mean_pulse_rate_bpm") is not None:
            observations.append(
                "A recording-level pulse-rate estimate "
                "is available."
            )

        if not observations:
            observations.append(
                "No physiological event features were "
                "available for interpretation."
            )

        assessment[signal_name] = {
            "evidence_type": "physiological_events",
            "observations": observations,
            "features_available": True
        }

    return assessment


def assess_multimodal(multimodal):
    """
    Summarize measurable ECG-PLETH temporal evidence.

    No claim is made about alarm validity.
    """

    global_data = multimodal.get("global", {})
    alarm_data = multimodal.get("alarm_window", {})

    observations = []

    global_matches = global_data.get(
        "matched_event_count"
    )

    global_ecg = global_data.get(
        "ecg_peak_count"
    )

    alarm_matches = alarm_data.get(
        "matched_beat_count"
    )

    alarm_ecg = alarm_data.get(
        "ecg_peak_count"
    )

    alarm_fraction = alarm_data.get(
        "matching_fraction"
    )

    alarm_delay = alarm_data.get(
        "ecg_pleth_delay_mean_seconds"
    )

    if global_matches is not None:
        observations.append(
            f"{global_matches} ECG-PLETH temporal "
            "matches were identified globally."
        )

    if global_ecg is not None:
        observations.append(
            f"{global_ecg} ECG events were evaluated "
            "for global temporal matching."
        )

    if (
        alarm_matches is not None
        and alarm_ecg is not None
    ):
        observations.append(
            f"{alarm_matches} of {alarm_ecg} ECG events "
            "were matched within the alarm-centered "
            "window."
        )

    if alarm_fraction is not None:
        observations.append(
            f"Alarm-window matching fraction: "
            f"{alarm_fraction:.3f}."
        )

    if alarm_delay is not None:
        observations.append(
            f"Mean ECG-PLETH temporal delay in the "
            f"alarm window: {alarm_delay:.3f} seconds."
        )

    return {
        "evidence_type": "multimodal_temporal",
        "observations": observations,
        "features_available": bool(observations)
    }


def assess_temporal_context(temporal_context):
    """
    Convert temporal measurements into descriptive
    before/after observations.
    """

    windows = temporal_context.get(
        "windows",
        {}
    )

    changes = temporal_context.get(
        "temporal_changes",
        {}
    )

    observations = []

    for window_name, window in windows.items():

        observations.append({
            "window": window_name,
            "ecg_events": window.get(
                "ecg_peak_count"
            ),
            "pleth_events": window.get(
                "pleth_pulse_count"
            ),
            "matched_events": window.get(
                "matched_event_count"
            ),
            "matching_fraction": window.get(
                "matching_fraction"
            ),
            "delay_seconds": window.get(
                "ecg_pleth_delay_mean_seconds"
            ),
            "heart_rate": window.get(
                "mean_heart_rate_bpm"
            ),
            "heart_rate_available": window.get(
                "heart_rate_available"
            )
        })

    temporal_changes = []

    for change_name, change in changes.items():

        temporal_changes.append({
            "comparison": change_name,
            "ecg_event_change": change.get(
                "ecg_peak_count"
            ),
            "pleth_event_change": change.get(
                "pleth_pulse_count"
            ),
            "matching_fraction_change": change.get(
                "matching_fraction"
            ),
            "delay_change_seconds": change.get(
                "ecg_pleth_delay_mean_seconds"
            ),
            "rr_variability_change": change.get(
                "rr_std_seconds"
            ),
            "heart_rate_change": change.get(
                "mean_heart_rate_bpm"
            )
        })

    return {
        "evidence_type": "temporal_context",
        "window_observations": observations,
        "temporal_changes": temporal_changes,
        "features_available": bool(observations)
    }


def build_evidence_assessment(event_name):

    episode_path = EPISODE_DIR / event_name

    evidence_profile = load_json(
        episode_path / "evidence_profile.json"
    )

    assessment = {
        "event": event_name,

        "purpose": (
            "Interpret measurable evidence without "
            "assigning a clinical credibility score."
        ),

        "signal_quality": assess_signal_quality(
            evidence_profile[
                "signal_quality_evidence"
            ]
        ),

        "physiological_evidence": assess_physiology(
            evidence_profile[
                "physiological_evidence"
            ]
        ),

        "multimodal_evidence": assess_multimodal(
            evidence_profile[
                "multimodal_evidence"
            ]
        ),

        "temporal_evidence": assess_temporal_context(
            evidence_profile[
                "temporal_context"
            ]
        )
    }

    return assessment


def save_assessment(event_name, assessment):

    episode_path = EPISODE_DIR / event_name

    output_path = (
        episode_path / "evidence_assessment.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            assessment,
            file,
            indent=4
        )

    return output_path


def print_summary(assessment, output_path):

    print()
    print("=" * 40)
    print("CLARIS - Evidence Assessment")
    print("=" * 40)

    print(
        f"Event: {assessment['event']}"
    )

    print()

    print("----------------------------------------")
    print("SIGNAL QUALITY")
    print("----------------------------------------")

    for signal_name, result in assessment[
        "signal_quality"
    ].items():

        print()
        print(f"  {signal_name}")

        for observation in result[
            "observations"
        ]:
            print(
                f"    - {observation}"
            )

    print()

    print("----------------------------------------")
    print("PHYSIOLOGICAL EVIDENCE")
    print("----------------------------------------")

    for signal_name, result in assessment[
        "physiological_evidence"
    ].items():

        print()
        print(f"  {signal_name}")

        for observation in result[
            "observations"
        ]:
            print(
                f"    - {observation}"
            )

    print()

    print("----------------------------------------")
    print("MULTIMODAL EVIDENCE")
    print("----------------------------------------")

    for observation in assessment[
        "multimodal_evidence"
    ]["observations"]:

        print(
            f"  - {observation}"
        )

    print()

    print("----------------------------------------")
    print("TEMPORAL EVIDENCE")
    print("----------------------------------------")

    temporal = assessment[
        "temporal_evidence"
    ]

    for observation in temporal[
        "window_observations"
    ]:

        print()
        print(
            f"  {observation['window']}"
        )

        print(
            f"    ECG events: "
            f"{observation['ecg_events']}"
        )

        print(
            f"    PLETH events: "
            f"{observation['pleth_events']}"
        )

        print(
            f"    Matched events: "
            f"{observation['matched_events']}"
        )

        print(
            f"    Matching fraction: "
            f"{observation['matching_fraction']}"
        )

        print(
            f"    Mean delay: "
            f"{observation['delay_seconds']}"
        )

        print(
            f"    HR available: "
            f"{observation['heart_rate_available']}"
        )

    print()

    print("----------------------------------------")
    print("OUTPUT")
    print("----------------------------------------")

    print(
        "No clinical credibility score assigned."
    )

    print()
    print(
        f"Saved to:\n{output_path}"
    )

    print()

    print("=" * 40)
    print("Evidence assessment complete.")
    print("=" * 40)


def main():

    event_name = "003c13_0115"

    assessment = build_evidence_assessment(
        event_name
    )

    output_path = save_assessment(
        event_name,
        assessment
    )

    print_summary(
        assessment,
        output_path
    )


if __name__ == "__main__":
    main()