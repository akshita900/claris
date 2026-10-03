
import json
from pathlib import Path
from datetime import datetime, timezone


EPISODE = "003c13_0115"

EPISODE_DIR = Path("data/episodes") / EPISODE

FILES = {
    "alarm_event": EPISODE_DIR / "alarm_event.json",
    "reasoning": EPISODE_DIR / "evidence_reasoning.json",
    "relationship": EPISODE_DIR / "evidence_relationship.json",
    "multimodal": EPISODE_DIR / "multimodal_evidence.json",
    "reliability": EPISODE_DIR / "evidence_reliability.json",
    "metadata": EPISODE_DIR / "metadata.json",
    "episode_validation": EPISODE_DIR / "episode_validation.json",
}

OUTPUT_FILE = EPISODE_DIR / "evidence_audit.json"

TOLERANCE = 1e-9

findings = []


def add_finding(check, status, detail):
    findings.append({
        "check": check,
        "status": status,
        "detail": detail
    })


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_value(data, path):
    current = data

    try:
        for key in path.split("."):
            current = current[key]
        return current
    except (KeyError, TypeError):
        return None


def values_equal(first, second):
    if first is None or second is None:
        return first is second

    if isinstance(first, (int, float)) and isinstance(
        second, (int, float)
    ):
        return abs(first - second) <= TOLERANCE

    return first == second


def compare_values(name, first, second, description):
    if first is None and second is None:
        add_finding(
            name,
            "passed",
            f"{description}: both representations are null."
        )
    elif values_equal(first, second):
        add_finding(
            name,
            "passed",
            f"{description}: values agree."
        )
    else:
        add_finding(
            name,
            "warning",
            f"{description}: values differ. "
            f"First={first}, second={second}."
        )


def compare_lists_by_key(
    name,
    first_list,
    second_list,
    key,
    fields
):
    if not isinstance(first_list, list) or not isinstance(
        second_list, list
    ):
        add_finding(
            name,
            "not_assessed",
            "One or both evidence collections are unavailable."
        )
        return

    first_map = {
        item.get(key): item
        for item in first_list
        if isinstance(item, dict)
    }

    second_map = {
        item.get(key): item
        for item in second_list
        if isinstance(item, dict)
    }

    if first_map.keys() != second_map.keys():
        add_finding(
            name,
            "warning",
            "Evidence identifiers differ between representations."
        )
        return

    differences = []

    for identifier in first_map:
        for field in fields:
            first_value = first_map[identifier].get(field)
            second_value = second_map[identifier].get(field)

            if not values_equal(first_value, second_value):
                differences.append(
                    f"{identifier}.{field}: "
                    f"{first_value} != {second_value}"
                )

    if differences:
        add_finding(
            name,
            "warning",
            "; ".join(differences)
        )
    else:
        add_finding(
            name,
            "passed",
            "Specified evidence fields agree across representations."
        )


def main():
    data = {}
    missing = []

    for name, path in FILES.items():
        if path.exists():
            try:
                data[name] = load_json(path)
            except (json.JSONDecodeError, OSError) as error:
                add_finding(
                    f"{name}_readable",
                    "warning",
                    f"Could not read JSON: {error}"
                )
        else:
            missing.append(name)

    if missing:
        add_finding(
            "source_files_available",
            "warning",
            f"Missing source files: {missing}"
        )
    else:
        add_finding(
            "source_files_available",
            "passed",
            "All configured source files are present."
        )

    alarm = data.get("alarm_event")
    reasoning = data.get("reasoning")
    relationship = data.get("relationship")
    multimodal = data.get("multimodal")
    reliability = data.get("reliability")
    metadata = data.get("metadata")

    # Episode identity and metadata traceability

    identity_sources = {
        name: get_value(source, "episode")
        for name, source in {
            "alarm_event": alarm,
            "reasoning": reasoning,
            "relationship": relationship,
        }.items()
        if source is not None
    }

    if multimodal is not None:
        identity_sources["multimodal"] = multimodal.get("event")

    if reliability is not None:
        identity_sources["reliability"] = reliability.get("event")

    if metadata is not None:
        identity_sources["metadata"] = metadata.get("event")

    if identity_sources and all(
        value == EPISODE for value in identity_sources.values()
    ):
        add_finding(
            "episode_identity_traceability",
            "passed",
            "Available source files identify the same episode."
        )
    else:
        add_finding(
            "episode_identity_traceability",
            "warning",
            f"Episode identity mismatch or missing identity: "
            f"{identity_sources}"
        )

    # Read metadata from each source using its actual schema.

    metadata_values = {}

    if alarm is not None:
        alarm_metadata = alarm.get("event_metadata", {})
        metadata_values["alarm_event"] = (
            alarm_metadata.get("sampling_frequency_hz"),
            alarm_metadata.get("alarm_reference_sample")
        )

    if multimodal is not None:
        metadata_values["multimodal"] = (
            multimodal.get("sampling_frequency_hz"),
            multimodal.get("alarm_reference_sample")
        )

    if reliability is not None:
        metadata_values["reliability"] = (
            reliability.get("sampling_frequency_hz"),
            reliability.get("alarm_reference_sample")
        )

    if metadata is not None:
        metadata_event_window = metadata.get("event_window", {})

        metadata_values["metadata"] = (
            metadata.get("sampling_frequency_hz"),
            metadata_event_window.get("alarm_reference_sample")
        )

    if metadata_values:
        reference_values = [
            value
            for pair in metadata_values.values()
            for value in pair
            if value is not None
        ]

        missing_metadata = {
            name: pair
            for name, pair in metadata_values.items()
            if any(value is None for value in pair)
        }

        if missing_metadata:
            add_finding(
                "sampling_and_alarm_reference_traceability",
                "warning",
                "One or more source representations lack required "
                f"metadata values: {missing_metadata}. "
                f"All available values: {metadata_values}"
            )
        else:
            unique_metadata = set(metadata_values.values())

            if len(unique_metadata) == 1:
                add_finding(
                    "sampling_and_alarm_reference_traceability",
                    "passed",
                    "Sampling frequency and alarm reference agree "
                    "across available representations."
                )
            else:
                add_finding(
                    "sampling_and_alarm_reference_traceability",
                    "warning",
                    f"Metadata differences detected: {metadata_values}"
                )
    else:
        add_finding(
            "sampling_and_alarm_reference_traceability",
            "not_assessed",
            "No metadata representations are available."
        )

    # Consolidated physiological evidence

    if alarm is not None and reasoning is not None:
        compare_lists_by_key(
            "physiological_evidence_traceability",
            alarm.get("physiological_evidence"),
            reasoning.get("physiological_reasoning"),
            "signal",
            [
                "modality",
                "observations"
            ]
        )

    # Multimodal evidence traceability

    if alarm is not None and reasoning is not None:
        alarm_multimodal = alarm.get("multimodal_evidence")
        reasoning_multimodal = reasoning.get("multimodal_reasoning")

        if (
            isinstance(alarm_multimodal, dict)
            and isinstance(reasoning_multimodal, dict)
        ):
            core_fields = [
                "signals_used",
                "global",
                "alarm_window"
            ]

            differences = []

            for field in core_fields:
                first_value = alarm_multimodal.get(field)
                second_value = reasoning_multimodal.get(field)

                if not values_equal(first_value, second_value):
                    differences.append(
                        f"{field}: {first_value} != {second_value}"
                    )

            if differences:
                add_finding(
                    "multimodal_reasoning_traceability",
                    "warning",
                    "; ".join(differences)
                )
            else:
                add_finding(
                    "multimodal_reasoning_traceability",
                    "passed",
                    "Core multimodal measurements agree. "
                    "Descriptive reasoning states and interpretation "
                    "boundaries are assessed separately."
                )
        else:
            add_finding(
                "multimodal_reasoning_traceability",
                "not_assessed",
                "One or both multimodal representations are unavailable."
            )

    if multimodal is not None and reliability is not None:
        raw_global = multimodal.get("global", {})
        reliability_global = get_value(
            reliability,
            "multimodal_evidence.global"
        ) or {}

        global_fields = {
            "ecg_peak_count": "ecg_peak_count",
            "pleth_peak_count": "pleth_peak_count",
            "matched_event_count": "matched_event_count",
            "mean_ecg_pleth_delay_seconds":
                "mean_ecg_pleth_delay_seconds",
            "std_ecg_pleth_delay_seconds":
                "std_ecg_pleth_delay_seconds",
        }

        for source_field, target_field in global_fields.items():
            compare_values(
                f"global_multimodal_{source_field}",
                raw_global.get(source_field),
                reliability_global.get(target_field),
                f"Global multimodal {source_field}"
            )

        raw_window = multimodal.get("alarm_window", {})
        reliability_window = get_value(
            reliability,
            "multimodal_evidence.alarm_window"
        ) or {}

        window_fields = [
            "ecg_peak_count",
            "pleth_peak_count",
            "matched_beat_count",
            "matching_fraction",
            "ecg_pleth_delay_mean_seconds",
            "ecg_pleth_delay_std_seconds",
        ]

        for field in window_fields:
            compare_values(
                f"alarm_window_{field}",
                raw_window.get(field),
                reliability_window.get(field),
                f"Alarm-window {field}"
            )

    # Temporal evidence traceability

    temporal_fields = [
        "window",
        "ecg_events",
        "pleth_events",
        "matched_events",
        "matching_fraction",
        "ecg_pleth_delay_seconds",
        "heart_rate",
        "heart_rate_available"
    ]

    if alarm is not None and reasoning is not None:
        compare_lists_by_key(
            "temporal_evidence_traceability",
            get_value(alarm, "temporal_evidence.windows"),
            reasoning.get("temporal_reasoning"),
            "window",
            temporal_fields
        )

    if alarm is not None and relationship is not None:
        compare_lists_by_key(
            "temporal_relationship_traceability",
            get_value(alarm, "temporal_evidence.windows"),
            relationship.get("temporal_relationships"),
            "window",
            [
                "window",
                "ecg_events",
                "pleth_events",
                "matched_events",
                "matching_fraction",
                "ecg_pleth_delay_seconds",
                "heart_rate",
                "heart_rate_available",
            ]
        )

    # Temporal changes

    change_fields = [
        "transition",
        "ecg_event_change",
        "pleth_event_change",
        "matching_fraction_change",
        "ecg_pleth_delay_change_seconds",
        "rr_variability_change_seconds",
        "heart_rate_change_bpm",
    ]

    if alarm is not None and reasoning is not None:
        compare_lists_by_key(
            "temporal_change_traceability",
            get_value(alarm, "temporal_evidence.changes"),
            reasoning.get("temporal_change_reasoning"),
            "transition",
            change_fields
        )

    if alarm is not None and relationship is not None:
        compare_lists_by_key(
            "temporal_relationship_change_traceability",
            get_value(alarm, "temporal_evidence.changes"),
            relationship.get("temporal_changes"),
            "transition",
            change_fields
        )

    # Missing-data semantics

    temporal_windows = get_value(
        alarm,
        "temporal_evidence.windows"
    ) if alarm else None

    if isinstance(temporal_windows, list):
        invalid_availability = []

        for window in temporal_windows:
            if (
                window.get("heart_rate_available") is False
                and window.get("heart_rate") is not None
            ):
                invalid_availability.append(
                    window.get("window")
                )

            if (
                window.get("heart_rate_available") is True
                and window.get("heart_rate") is None
            ):
                invalid_availability.append(
                    window.get("window")
                )

        if invalid_availability:
            add_finding(
                "missing_data_semantics",
                "warning",
                "Heart-rate value and availability flag "
                f"are inconsistent in: {invalid_availability}"
            )
        else:
            add_finding(
                "missing_data_semantics",
                "passed",
                "Heart-rate null values agree with availability flags."
            )
    else:
        add_finding(
            "missing_data_semantics",
            "not_assessed",
            "Temporal window data are unavailable."
        )

    # Scope separation

    if multimodal is not None:
        global_data = multimodal.get("global")
        window_data = multimodal.get("alarm_window")

        if isinstance(global_data, dict) and isinstance(
            window_data, dict
        ):
            add_finding(
                "evidence_scope_separation",
                "passed",
                "Global and alarm-window evidence are retained "
                "as separate scopes. Their counts are not assumed "
                "to be additive or interchangeable."
            )
        else:
            add_finding(
                "evidence_scope_separation",
                "not_assessed",
                "Global or alarm-window evidence is unavailable."
            )

    # Clinical boundary

    boundary_checks = []

    if alarm is not None:
        boundary = alarm.get("clinical_boundary", {})
        boundary_checks.extend([
            boundary.get("credibility_score") is None,
            boundary.get("clinical_decision") is None,
        ])

    if reasoning is not None:
        boundary_checks.append(
            reasoning.get("clinical_decision") is None
        )

        credibility = reasoning.get(
            "credibility_assessment", {}
        )

        boundary_checks.append(
            credibility.get("status") in {
                "not_assigned",
                "not_assessed",
                "unassigned",
            }
        )

    if relationship is not None:
        boundary_checks.extend([
            relationship.get("credibility_score") is None,
            relationship.get("clinical_decision") is None,
        ])

    if reliability is not None:
        interpretation = reliability.get(
            "reliability_interpretation", {}
        )

        boundary_checks.extend([
            interpretation.get("alarm_credibility_score") is None,
            interpretation.get("clinical_decision") is None,
        ])

    if boundary_checks and all(boundary_checks):
        add_finding(
            "clinical_boundary_preserved",
            "passed",
            "No credibility score or clinical decision is assigned "
            "in the audited representations."
        )
    else:
        add_finding(
            "clinical_boundary_preserved",
            "warning",
            "A clinical-boundary field is assigned, missing, "
            "or uses an unrecognized status. Manual review required."
        )

    # Audit summary

    counts = {
        "passed": sum(
            item["status"] == "passed" for item in findings
        ),
        "warning": sum(
            item["status"] == "warning" for item in findings
        ),
        "not_assessed": sum(
            item["status"] == "not_assessed" for item in findings
        ),
    }

    audit_state = (
        "review_required"
        if counts["warning"] > 0
        else "descriptive_audit_complete"
    )

    report = {
        "project": "CLARIS",
        "module": "Evidence Audit",
        "episode": EPISODE,
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "audit_scope": [
            "source availability",
            "episode identity",
            "metadata traceability",
            "physiological evidence traceability",
            "multimodal evidence traceability",
            "temporal evidence traceability",
            "missing-data semantics",
            "evidence scope separation",
            "clinical boundary preservation",
        ],
        "findings": findings,
        "summary": {
            "total_findings": len(findings),
            **counts,
            "audit_state": audit_state,
        },
        "clinical_boundary": {
            "alarm_credibility_score": None,
            "clinical_decision": None,
            "interpretation": (
                "This audit evaluates data consistency and "
                "traceability only. It does not establish "
                "clinical alarm validity."
            ),
        },
        "limitations": [
            "The audit uses existing generated JSON files.",
            "It does not independently validate detector accuracy.",
            "It does not establish physiological or clinical truth.",
            "Matching correspondence is not alarm credibility.",
            "Temporal association does not establish causation.",
            "A single episode cannot establish general performance.",
        ],
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nCLARIS - Evidence Audit")
    print("----------------------")
    print(f"Episode: {EPISODE}")
    print(f"Total findings: {len(findings)}")
    print(f"Passed: {counts['passed']}")
    print(f"Warnings: {counts['warning']}")
    print(f"Not assessed: {counts['not_assessed']}")
    print(f"Audit state: {audit_state}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
