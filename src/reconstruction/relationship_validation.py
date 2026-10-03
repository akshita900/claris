
import json
import math
from numbers import Real
from pathlib import Path


EPISODE_DIR = Path("data/episodes/003c13_0115")
INPUT_FILE = EPISODE_DIR / "evidence_relationship.json"
OUTPUT_FILE = EPISODE_DIR / "relationship_validation.json"

TOLERANCE = 1e-9


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def add_check(checks, name, passed, details):
    checks.append({
        "check": name,
        "passed": bool(passed),
        "details": details
    })


def is_finite_number(value):
    return (
        isinstance(value, Real)
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def is_valid_count(value):
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value >= 0
    )


def is_valid_measurement(value, minimum=None, maximum=None):
    if not is_finite_number(value):
        return False

    if minimum is not None and value < minimum:
        return False

    if maximum is not None and value > maximum:
        return False

    return True


def values_match(actual, expected):
    if actual is None or expected is None:
        return actual is None and expected is None

    if not is_finite_number(actual) or not is_finite_number(expected):
        return False

    return abs(actual - expected) <= TOLERANCE


def validate_physiological_evidence(data, checks):
    physiological = data.get("physiological_evidence", [])

    valid = isinstance(physiological, list)
    problems = []

    if not valid:
        physiological = []
        problems.append("physiological_evidence must be a list")

    for item in physiological:
        if not isinstance(item, dict):
            valid = False
            problems.append("Invalid physiological evidence entry")
            continue

        signal = item.get("signal", "unknown")
        event_count = item.get("event_count")
        local_event_count = item.get("local_event_count")

        if not is_valid_count(event_count):
            valid = False
            problems.append(f"{signal}: invalid event_count")

        if not is_valid_count(local_event_count):
            valid = False
            problems.append(f"{signal}: invalid local_event_count")

        if (
            is_valid_count(event_count)
            and is_valid_count(local_event_count)
            and local_event_count > event_count
        ):
            valid = False
            problems.append(
                f"{signal}: local_event_count exceeds event_count"
            )

        for field in (
            "mean_heart_rate_bpm",
            "mean_pulse_rate_bpm"
        ):
            value = item.get(field)

            if value is not None and not is_valid_measurement(value, 0):
                valid = False
                problems.append(f"{signal}: invalid {field}")

    add_check(
        checks,
        "physiological_event_counts",
        valid,
        "Physiological counts and available rate measurements are structurally valid."
        if valid
        else "; ".join(problems)
    )


def validate_multimodal_relationship(data, checks):
    multimodal = data.get("multimodal_relationship", {})

    valid = isinstance(multimodal, dict)
    problems = []

    if not valid:
        multimodal = {}
        problems.append("multimodal_relationship must be an object")

    global_rel = multimodal.get("global_relationship", {})
    alarm_rel = multimodal.get("alarm_window_relationship", {})

    if not isinstance(global_rel, dict):
        global_rel = {}
        valid = False
        problems.append("Invalid global_relationship object")

    if not isinstance(alarm_rel, dict):
        alarm_rel = {}
        valid = False
        problems.append("Invalid alarm_window_relationship object")

    matched_global = global_rel.get("matched_events")
    global_delay = global_rel.get("mean_delay_seconds")

    alarm_ecg = alarm_rel.get("ecg_events")
    alarm_matched = alarm_rel.get("matched_events")
    alarm_fraction = alarm_rel.get("matching_fraction")
    alarm_delay = alarm_rel.get("mean_delay_seconds")

    if not is_valid_count(matched_global):
        valid = False
        problems.append("Invalid global matched_events")

    if global_delay is not None and not is_valid_measurement(global_delay, 0):
        valid = False
        problems.append("Invalid global mean delay")

    if not is_valid_count(alarm_ecg):
        valid = False
        problems.append("Invalid alarm ECG event count")

    if not is_valid_count(alarm_matched):
        valid = False
        problems.append("Invalid alarm matched event count")

    pleth_count = alarm_rel.get("pleth_events")

    if pleth_count is not None and not is_valid_count(pleth_count):
        valid = False
        problems.append("Invalid alarm PLETH event count")

    if (
        is_valid_count(alarm_matched)
        and is_valid_count(alarm_ecg)
        and alarm_matched > alarm_ecg
    ):
        valid = False
        problems.append("Alarm matched events exceed ECG events")

    if (
        pleth_count is not None
        and is_valid_count(alarm_matched)
        and is_valid_count(pleth_count)
        and alarm_matched > pleth_count
    ):
        valid = False
        problems.append("Alarm matched events exceed PLETH events")

    if alarm_ecg == 0:
        if alarm_matched == 0 and alarm_fraction is not None:
            valid = False
            problems.append(
                "Matching fraction must be null when ECG denominator is zero"
            )
    elif is_valid_count(alarm_ecg) and is_valid_count(alarm_matched):
        expected_fraction = alarm_matched / alarm_ecg

        if not is_valid_measurement(alarm_fraction, 0, 1):
            valid = False
            problems.append("Invalid alarm matching fraction")
        elif not values_match(alarm_fraction, expected_fraction):
            valid = False
            problems.append("Alarm matching fraction is inconsistent")

    if alarm_delay is not None and not is_valid_measurement(alarm_delay, 0):
        valid = False
        problems.append("Invalid alarm-window mean delay")

    delay_std = alarm_rel.get("delay_std_seconds")

    if delay_std is not None and not is_valid_measurement(delay_std, 0):
        valid = False
        problems.append("Invalid alarm-window delay standard deviation")

    if alarm_matched == 0 and alarm_delay is not None:
        valid = False
        problems.append(
            "Alarm delay should be null when no events are matched"
        )

    add_check(
        checks,
        "multimodal_relationship_consistency",
        valid,
        "Multimodal counts, matching fraction, and available delays are internally consistent."
        if valid
        else "; ".join(problems)
    )


def validate_temporal_relationships(data, checks):
    temporal = data.get("temporal_relationships", [])

    valid = isinstance(temporal, list)
    problems = []

    if not valid:
        temporal = []
        problems.append("temporal_relationships must be a list")

    for item in temporal:
        if not isinstance(item, dict):
            valid = False
            problems.append("Invalid temporal relationship entry")
            continue

        window = item.get("window", "unknown")

        ecg = item.get("ecg_events")
        pleth = item.get("pleth_events")
        matched = item.get("matched_events")
        fraction = item.get("matching_fraction")
        delay = item.get("ecg_pleth_delay_seconds")

        for name, value in (
            ("ECG", ecg),
            ("PLETH", pleth),
            ("matched", matched)
        ):
            if not is_valid_count(value):
                valid = False
                problems.append(f"{window}: invalid {name} event count")

        if (
            is_valid_count(matched)
            and is_valid_count(ecg)
            and matched > ecg
        ):
            valid = False
            problems.append(f"{window}: matched events exceed ECG events")

        if (
            is_valid_count(matched)
            and is_valid_count(pleth)
            and matched > pleth
        ):
            valid = False
            problems.append(f"{window}: matched events exceed PLETH events")

        if ecg == 0:
            if matched == 0 and fraction is not None:
                valid = False
                problems.append(
                    f"{window}: fraction must be null with zero ECG events"
                )
        elif is_valid_count(ecg) and is_valid_count(matched):
            expected_fraction = matched / ecg

            if not is_valid_measurement(fraction, 0, 1):
                valid = False
                problems.append(f"{window}: invalid matching fraction")
            elif not values_match(fraction, expected_fraction):
                valid = False
                problems.append(
                    f"{window}: matching fraction is inconsistent"
                )

        if delay is not None and not is_valid_measurement(delay, 0):
            valid = False
            problems.append(f"{window}: invalid ECG-PLETH delay")

        if matched == 0 and delay is not None:
            valid = False
            problems.append(
                f"{window}: delay should be null when no events are matched"
            )

        heart_rate = item.get("heart_rate")
        heart_rate_available = item.get("heart_rate_available")

        if not isinstance(heart_rate_available, bool):
            valid = False
            problems.append(
                f"{window}: heart_rate_available must be boolean"
            )
        elif heart_rate_available:
            if not is_valid_measurement(heart_rate, 0):
                valid = False
                problems.append(
                    f"{window}: available heart rate is invalid"
                )
        elif heart_rate is not None:
            valid = False
            problems.append(
                f"{window}: unavailable heart rate must be null"
            )

        state = item.get("relationship_state")

        if state not in ("relationship_observed", "relationship_not_available"):
            valid = False
            problems.append(f"{window}: invalid relationship_state")
        elif state == "relationship_observed":
            if not is_valid_count(matched) or matched == 0:
                valid = False
                problems.append(
                    f"{window}: observed state requires matched events"
                )
        elif is_valid_count(matched) and matched > 0:
            valid = False
            problems.append(
                f"{window}: unavailable state conflicts with matched events"
            )

    add_check(
        checks,
        "temporal_relationship_consistency",
        valid,
        "Temporal counts, fractions, delays, and availability states are consistent."
        if valid
        else "; ".join(problems)
    )


def validate_temporal_changes(data, checks):
    temporal = data.get("temporal_relationships", [])
    changes = data.get("temporal_changes", [])

    valid = isinstance(temporal, list) and isinstance(changes, list)
    problems = []

    if not valid:
        temporal = temporal if isinstance(temporal, list) else []
        changes = changes if isinstance(changes, list) else []
        problems.append("Temporal relationships and changes must be lists")

    if len(changes) != max(0, len(temporal) - 1):
        valid = False
        problems.append(
            "Number of transitions does not match temporal windows"
        )

    fields = (
        ("ecg_events", "ecg_event_change", True),
        ("pleth_events", "pleth_event_change", True),
        ("matching_fraction", "matching_fraction_change", False),
        ("ecg_pleth_delay_seconds", "ecg_pleth_delay_change_seconds", False)
    )

    for index, change in enumerate(changes):
        if index + 1 >= len(temporal):
            break

        if not isinstance(change, dict):
            valid = False
            problems.append(f"Transition {index}: invalid change object")
            continue

        first = temporal[index]
        second = temporal[index + 1]

        if not isinstance(first, dict) or not isinstance(second, dict):
            valid = False
            problems.append(f"Transition {index}: invalid window object")
            continue

        transition = change.get("transition", f"transition_{index}")

        for source_field, change_field, integer_field in fields:
            first_value = first.get(source_field)
            second_value = second.get(source_field)
            actual = change.get(change_field)

            if first_value is None or second_value is None:
                if actual is not None:
                    valid = False
                    problems.append(
                        f"{transition}: {change_field} must be null "
                        "when a source value is unavailable"
                    )
                continue

            if not is_finite_number(first_value) or not is_finite_number(second_value):
                valid = False
                problems.append(
                    f"{transition}: invalid source values for {change_field}"
                )
                continue

            expected = second_value - first_value

            if integer_field:
                if not is_valid_count(first_value) or not is_valid_count(second_value):
                    valid = False
                    problems.append(
                        f"{transition}: invalid count source for {change_field}"
                    )
                    continue

                if actual != expected or isinstance(actual, bool):
                    valid = False
                    problems.append(
                        f"{transition}: {change_field} is inconsistent"
                    )
            elif not values_match(actual, expected):
                valid = False
                problems.append(
                    f"{transition}: {change_field} is inconsistent"
                )

    add_check(
        checks,
        "temporal_change_consistency",
        valid,
        "Available temporal transition values match adjacent-window differences."
        if valid
        else "; ".join(problems)
    )


def validate_relationship_state(data, checks):
    summary = data.get("relationship_summary", {})
    multimodal = data.get("multimodal_relationship", {})
    temporal = data.get("temporal_relationships", [])
    changes = data.get("temporal_changes", [])

    valid = isinstance(summary, dict)
    problems = []

    if not valid:
        summary = {}
        problems.append("relationship_summary must be an object")

    fields = (
        "multimodal_relationship_observed",
        "temporal_context_observed",
        "temporal_changes_available"
    )

    for field in fields:
        if not isinstance(summary.get(field), bool):
            valid = False
            problems.append(f"{field} must be boolean")

    alarm = (
        multimodal.get("alarm_window_relationship", {})
        if isinstance(multimodal, dict)
        else {}
    )

    if isinstance(alarm, dict):
        matched = alarm.get("matched_events")
        expected_multimodal = is_valid_count(matched) and matched > 0

        if (
            isinstance(summary.get("multimodal_relationship_observed"), bool)
            and summary["multimodal_relationship_observed"] != expected_multimodal
        ):
            valid = False
            problems.append(
                "Multimodal summary conflicts with alarm-window matched events"
            )

    if isinstance(temporal, list):
        expected_temporal = any(
            isinstance(item, dict)
            and is_valid_count(item.get("matched_events"))
            and item["matched_events"] > 0
            for item in temporal
        )

        if (
            isinstance(summary.get("temporal_context_observed"), bool)
            and summary["temporal_context_observed"] != expected_temporal
        ):
            valid = False
            problems.append(
                "Temporal summary conflicts with temporal evidence"
            )

    if isinstance(changes, list):
        expected_changes = len(changes) > 0

        if (
            isinstance(summary.get("temporal_changes_available"), bool)
            and summary["temporal_changes_available"] != expected_changes
        ):
            valid = False
            problems.append(
                "Temporal changes summary conflicts with transition data"
            )

    add_check(
        checks,
        "relationship_state_structure",
        valid,
        "Relationship summary flags are explicit and consistent with available evidence."
        if valid
        else "; ".join(problems)
    )


def validate_clinical_boundary(data, checks):
    valid = (
        data.get("credibility_score") is None
        and data.get("clinical_decision") is None
    )

    add_check(
        checks,
        "clinical_boundary_preserved",
        valid,
        "No alarm credibility score or clinical decision is assigned."
        if valid
        else "Clinical credibility or decision fields contain a value."
    )


def build_validation_profile(data):
    checks = []

    validate_physiological_evidence(data, checks)
    validate_multimodal_relationship(data, checks)
    validate_temporal_relationships(data, checks)
    validate_temporal_changes(data, checks)
    validate_relationship_state(data, checks)
    validate_clinical_boundary(data, checks)

    passed_checks = sum(1 for check in checks if check["passed"])
    failed_checks = len(checks) - passed_checks

    return {
        "episode": data.get("episode"),
        "purpose": (
            "Validate internal consistency of measured physiological "
            "relationships and temporal evidence without assigning "
            "alarm credibility or making a clinical decision."
        ),
        "checks": checks,
        "validation_summary": {
            "total_checks": len(checks),
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "validation_state": (
                "passed" if failed_checks == 0 else "issues_detected"
            )
        },
        "credibility_score": None,
        "clinical_decision": None
    }


def save_validation_profile(profile):
    EPISODE_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4, allow_nan=False)

    print(f"Output: {OUTPUT_FILE}")


def main():
    data = load_json(INPUT_FILE)
    profile = build_validation_profile(data)
    save_validation_profile(profile)

    summary = profile["validation_summary"]
    print(
        f"Validation: {summary['validation_state']} | "
        f"Passed: {summary['passed_checks']}/"
        f"{summary['total_checks']}"
    )

    for check in profile["checks"]:
        if not check["passed"]:
            print(f"FAILED: {check['check']} — {check['details']}")


if __name__ == "__main__":
    main()
