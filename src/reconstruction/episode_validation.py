import json
from pathlib import Path


EPISODE_DIR = Path("data/episodes/003c13_0115")

METADATA_FILE = EPISODE_DIR / "metadata.json"
SIGNAL_QUALITY_FILE = EPISODE_DIR / "signal_quality.json"
PHYSIOLOGICAL_FILE = EPISODE_DIR / "physiological_features.json"
MULTIMODAL_FILE = EPISODE_DIR / "multimodal_evidence.json"
ALARM_CONTEXT_FILE = EPISODE_DIR / "alarm_context.json"
EVIDENCE_PROFILE_FILE = EPISODE_DIR / "evidence_profile.json"
EVIDENCE_REASONING_FILE = EPISODE_DIR / "evidence_reasoning.json"
ALARM_EVENT_FILE = EPISODE_DIR / "alarm_event.json"

OUTPUT_FILE = EPISODE_DIR / "episode_validation.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_file_exists(path):
    return path.exists()


def validate_metadata(metadata):
    required_fields = [
        "event",
        "sampling_frequency_hz",
    ]

    return all(
        field in metadata
        for field in required_fields
    )


def validate_alarm_reference(alarm_event):
    metadata = alarm_event["event_metadata"]

    required_fields = [
        "sampling_frequency_hz",
        "alarm_reference_sample",
        "alarm_reference_time_seconds",
    ]

    if not all(
        field in metadata
        for field in required_fields
    ):
        return False

    sampling_frequency = metadata[
        "sampling_frequency_hz"
    ]

    alarm_sample = metadata[
        "alarm_reference_sample"
    ]

    alarm_time = metadata[
        "alarm_reference_time_seconds"
    ]

    expected_time = (
        alarm_sample / sampling_frequency
    )

    return abs(
        expected_time - alarm_time
    ) < 1e-9


def validate_episode_identity(
    metadata,
    alarm_event,
):
    return (
        metadata["event"]
        == alarm_event["episode"]
        == "003c13_0115"
    )


def validate_sampling_frequency(
    metadata,
    alarm_event,
):
    return (
        metadata["sampling_frequency_hz"]
        == alarm_event["event_metadata"][
            "sampling_frequency_hz"
        ]
    )


def validate_signals(alarm_event):
    required_signals = {
        "II",
        "aVR",
        "V",
        "PLETH",
    }

    available_signals = set(
        alarm_event["signals"]["available"]
    )

    return required_signals.issubset(
        available_signals
    )


def validate_physiological_evidence(alarm_event):
    evidence = alarm_event[
        "physiological_evidence"
    ]

    required_signals = {
        "II",
        "aVR",
        "V",
        "PLETH",
    }

    observed_signals = {
        item["signal"]
        for item in evidence
    }

    return observed_signals == required_signals


def validate_multimodal_evidence(alarm_event):
    multimodal = alarm_event[
        "multimodal_evidence"
    ]

    signals_used = multimodal[
        "signals_used"
    ]

    if signals_used.get("ecg") != "II":
        return False

    if signals_used.get("pleth") != "PLETH":
        return False

    alarm_window = multimodal[
        "alarm_window_observation"
    ]

    ecg_events = alarm_window[
        "ecg_events"
    ]

    matched_events = alarm_window[
        "matched_events"
    ]

    matching_fraction = alarm_window[
        "matching_fraction"
    ]

    if matched_events > ecg_events:
        return False

    if ecg_events == 0:
        expected_fraction = 0.0
    else:
        expected_fraction = (
            matched_events / ecg_events
        )

    return abs(
        expected_fraction
        - matching_fraction
    ) < 1e-9


def validate_temporal_evidence(alarm_event):
    temporal = alarm_event[
        "temporal_evidence"
    ]

    windows = temporal["windows"]

    expected_windows = [
        "pre_10_to_5",
        "pre_5_to_0",
        "post_0_to_5",
        "post_5_to_10",
    ]

    observed_windows = [
        window["window"]
        for window in windows
    ]

    if observed_windows != expected_windows:
        return False

    for window in windows:
        ecg_events = window[
            "ecg_events"
        ]

        matched_events = window[
            "matched_events"
        ]

        matching_fraction = window[
            "matching_fraction"
        ]

        if matched_events > ecg_events:
            return False

        if ecg_events == 0:
            expected_fraction = 0.0
        else:
            expected_fraction = (
                matched_events / ecg_events
            )

        if abs(
            expected_fraction
            - matching_fraction
        ) >= 1e-9:
            return False

    return True


def validate_temporal_changes(alarm_event):
    temporal = alarm_event[
        "temporal_evidence"
    ]

    windows = temporal["windows"]
    changes = temporal["changes"]

    if len(changes) != len(windows) - 1:
        return False

    for index, change in enumerate(changes):
        current_window = windows[index]
        next_window = windows[index + 1]

        expected_ecg_change = (
            next_window["ecg_events"]
            - current_window["ecg_events"]
        )

        expected_pleth_change = (
            next_window["pleth_events"]
            - current_window["pleth_events"]
        )

        expected_matching_change = (
            next_window["matching_fraction"]
            - current_window["matching_fraction"]
        )

        if (
            change["ecg_event_change"]
            != expected_ecg_change
        ):
            return False

        if (
            change["pleth_event_change"]
            != expected_pleth_change
        ):
            return False

        if abs(
            change["matching_fraction_change"]
            - expected_matching_change
        ) >= 1e-9:
            return False

    return True


def validate_reasoning_summary(alarm_event):
    summary = alarm_event[
        "reasoning_summary"
    ]

    required_fields = [
        "physiological_evidence_available",
        "multimodal_relationship_available",
        "temporal_context_available",
        "temporal_changes_available",
        "reasoning_state",
    ]

    if not all(
        field in summary
        for field in required_fields
    ):
        return False

    return (
        summary["reasoning_state"]
        == "evidence_reasoning_available"
    )


def validate_clinical_boundary(alarm_event):
    boundary = alarm_event[
        "clinical_boundary"
    ]

    return (
        boundary["credibility_score"] is None
        and boundary["clinical_decision"] is None
        and boundary["credibility_status"]
        == "not_assigned"
    )


def build_validation_report(results):
    total_checks = len(results)

    passed_checks = sum(
        1
        for result in results.values()
        if result
    )

    failed_checks = (
        total_checks - passed_checks
    )

    validation_state = (
        "passed"
        if failed_checks == 0
        else "failed"
    )

    return {
        "episode": "003c13_0115",
        "validation_scope": (
            "Complete reconstructed alarm episode"
        ),
        "checks": results,
        "summary": {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "validation_state": validation_state,
        },
        "clinical_boundary": {
            "credibility_score": None,
            "clinical_decision": None,
        },
    }


def main():
    metadata = load_json(
        METADATA_FILE
    )

    alarm_event = load_json(
        ALARM_EVENT_FILE
    )

    required_files = {
        "metadata": METADATA_FILE,
        "signal_quality": SIGNAL_QUALITY_FILE,
        "physiological_features": PHYSIOLOGICAL_FILE,
        "multimodal_evidence": MULTIMODAL_FILE,
        "alarm_context": ALARM_CONTEXT_FILE,
        "evidence_profile": EVIDENCE_PROFILE_FILE,
        "evidence_reasoning": EVIDENCE_REASONING_FILE,
        "alarm_event": ALARM_EVENT_FILE,
    }

    results = {}

    results["required_files_present"] = all(
        check_file_exists(path)
        for path in required_files.values()
    )

    results["metadata_structure_valid"] = (
        validate_metadata(metadata)
    )

    results["episode_identity_consistent"] = (
        validate_episode_identity(
            metadata,
            alarm_event,
        )
    )

    results["sampling_frequency_consistent"] = (
        validate_sampling_frequency(
            metadata,
            alarm_event,
        )
    )

    results["alarm_reference_consistent"] = (
        validate_alarm_reference(
            alarm_event,
        )
    )

    results["signal_set_complete"] = (
        validate_signals(alarm_event)
    )

    results[
        "physiological_evidence_complete"
    ] = (
        validate_physiological_evidence(
            alarm_event,
        )
    )

    results[
        "multimodal_evidence_consistent"
    ] = (
        validate_multimodal_evidence(
            alarm_event,
        )
    )

    results[
        "temporal_evidence_consistent"
    ] = (
        validate_temporal_evidence(
            alarm_event,
        )
    )

    results[
        "temporal_changes_consistent"
    ] = (
        validate_temporal_changes(
            alarm_event,
        )
    )

    results[
        "reasoning_summary_valid"
    ] = (
        validate_reasoning_summary(
            alarm_event,
        )
    )

    results[
        "clinical_boundary_preserved"
    ] = (
        validate_clinical_boundary(
            alarm_event,
        )
    )

    report = build_validation_report(
        results
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            report,
            f,
            indent=4,
        )

    print(
        f"Output: {OUTPUT_FILE}"
    )

    print(
        "Validation: "
        f"{report['summary']['validation_state']}"
    )


if __name__ == "__main__":
    main()