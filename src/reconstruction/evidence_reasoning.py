
import json
from pathlib import Path


EPISODE_DIR = Path("data/episodes/003c13_0115")

INPUT_FILE = EPISODE_DIR / "relationship_validation.json"
RELATIONSHIP_FILE = EPISODE_DIR / "evidence_relationship.json"
INTERPRETATION_FILE = EPISODE_DIR / "evidence_interpretation.json"

OUTPUT_FILE = EPISODE_DIR / "evidence_reasoning.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def reason_physiological_evidence(interpretation):
    physiological = interpretation.get(
        "physiological_evidence", []
    )

    reasoning = []

    for item in physiological:
        signal = item.get("signal")
        modality = item.get("modality")

        event_count = item.get("event_count")
        local_event_count = item.get("local_event_count")

        mean_hr = item.get("mean_heart_rate_bpm")
        mean_pulse = item.get("mean_pulse_rate_bpm")

        measurements_available = any(
            value is not None
            for value in (
                event_count,
                local_event_count,
                mean_hr,
                mean_pulse,
            )
        )

        reasoning.append({
            "signal": signal,
            "modality": modality,

            "observations": {
                "global_event_count": event_count,
                "local_event_count": local_event_count,
                "mean_heart_rate_bpm": mean_hr,
                "mean_pulse_rate_bpm": mean_pulse,
            },

            "reasoning_state": (
                "signal_derived_measurements_available"
                if measurements_available
                else "measurements_unavailable"
            ),

            "interpretation_boundary": (
                "Signal-derived measurements are descriptive "
                "and do not independently establish physiological "
                "or clinical validity."
            ),
        })

    return reasoning


def reason_multimodal_evidence(relationship):
    multimodal = relationship.get(
        "multimodal_relationship", {}
    )

    global_relationship = multimodal.get(
        "global_relationship", {}
    )

    alarm_relationship = multimodal.get(
        "alarm_window_relationship", {}
    )

    matched_events = alarm_relationship.get("matched_events")

    return {
        "signals_used": multimodal.get("signals_used"),

        "global_observation": {
            "matched_events":
                global_relationship.get("matched_events"),

            "mean_delay_seconds":
                global_relationship.get("mean_delay_seconds"),
        },

        "alarm_window_observation": {
            "ecg_events":
                alarm_relationship.get("ecg_events"),

            "matched_events": matched_events,

            "matching_fraction":
                alarm_relationship.get("matching_fraction"),

            "mean_delay_seconds":
                alarm_relationship.get("mean_delay_seconds"),

            "delay_std_seconds":
                alarm_relationship.get("delay_std_seconds"),
        },

        "reasoning_state": (
            "computed_temporal_association_available"
            if matched_events is not None
            else "relationship_measurement_unavailable"
        ),

        "interpretation_boundary": (
            "The computed ECG-PLETH association is descriptive. "
            "It does not establish causation, clinical validity, "
            "or alarm credibility."
        ),
    }


def reason_temporal_context(relationship):
    temporal = relationship.get(
        "temporal_relationships", []
    )

    results = []

    for item in temporal:
        heart_rate_available = item.get(
            "heart_rate_available"
        )

        matched_events = item.get("matched_events")

        if matched_events is None:
            state = "relationship_measurement_unavailable"
        elif matched_events < 3:
            state = "sparse_relationship_evidence"
        elif heart_rate_available is False:
            state = "relationship_observed_rate_unavailable"
        else:
            state = "relationship_observed_measurements_available"

        results.append({
            "window": item.get("window"),

            "ecg_events": item.get("ecg_events"),
            "pleth_events": item.get("pleth_events"),
            "matched_events": matched_events,

            "matching_fraction":
                item.get("matching_fraction"),

            "ecg_pleth_delay_seconds":
                item.get("ecg_pleth_delay_seconds"),

            "heart_rate": item.get("heart_rate"),

            "heart_rate_available": heart_rate_available,

            "reasoning_state": state,

            "interpretation_boundary": (
                "Window-level measurements are descriptive. "
                "Sparse event counts may limit rate and relationship "
                "estimation."
            ),
        })

    return results


def reason_temporal_changes(relationship):
    changes = relationship.get(
        "temporal_changes", []
    )

    results = []

    for item in changes:
        results.append({
            "transition": item.get("transition"),

            "ecg_event_change":
                item.get("ecg_event_change"),

            "pleth_event_change":
                item.get("pleth_event_change"),

            "matching_fraction_change":
                item.get("matching_fraction_change"),

            "ecg_pleth_delay_change_seconds":
                item.get("ecg_pleth_delay_change_seconds"),

            "rr_variability_change_seconds":
                item.get("rr_variability_change_seconds"),

            "heart_rate_change_bpm":
                item.get("heart_rate_change_bpm"),

            "interpretation_boundary": (
                "Changes describe differences between computed "
                "window-level measurements and do not independently "
                "establish physiological deterioration or improvement."
            ),
        })

    return results


def build_observations(
    physiological,
    multimodal,
    temporal,
    temporal_changes
):
    observations = []

    if physiological:
        observations.append(
            "Signal-derived measurements are available across "
            "multiple physiological evidence streams."
        )

    if multimodal.get("reasoning_state") == (
        "computed_temporal_association_available"
    ):
        observations.append(
            "A computed temporal association between ECG II "
            "and PLETH is available for descriptive examination."
        )

    if temporal:
        observations.append(
            "Alarm-centered temporal measurements are represented "
            "across multiple windows."
        )

    if temporal_changes:
        observations.append(
            "Differences between adjacent temporal-window "
            "measurements are available for descriptive examination."
        )

    return observations


def build_limitations(validation):
    limitations = []

    validation_summary = validation.get(
        "validation_summary", {}
    )

    validation_passed = (
        validation_summary.get("validation_state") == "passed"
    )

    if validation_passed:
        limitations.append(
            "Internal structural and arithmetic consistency checks "
            "passed. This does not establish scientific or clinical validity."
        )
    else:
        limitations.append(
            "Internal relationship validation identified issues. "
            "Downstream evidence interpretation requires caution."
        )

    limitations.extend([
        "Physiological measurements are signal-derived and descriptive.",
        "Temporal association does not establish causation.",
        "Sparse temporal windows may limit rate and relationship estimation.",
        "Signal quality and measurement uncertainty require separate assessment.",
        "Scientific validity of the observed relationships has not been established.",
        "Clinical validity has not been established.",
        "Observed relationships do not establish alarm validity.",
        "No alarm credibility score is assigned.",
        "No clinical decision is generated.",
    ])

    return limitations


def build_reasoning_profile(
    relationship,
    interpretation,
    validation
):
    physiological = reason_physiological_evidence(
        interpretation
    )

    multimodal = reason_multimodal_evidence(
        relationship
    )

    temporal = reason_temporal_context(
        relationship
    )

    temporal_changes = reason_temporal_changes(
        relationship
    )

    observations = build_observations(
        physiological,
        multimodal,
        temporal,
        temporal_changes
    )

    limitations = build_limitations(validation)

    validation_passed = (
        validation.get(
            "validation_summary", {}
        ).get("validation_state") == "passed"
    )

    reasoning_state = (
        "descriptive_evidence_available"
        if validation_passed and observations
        else "descriptive_evidence_limited"
    )

    return {
        "episode": relationship.get("episode"),

        "purpose": (
            "Describe signal-derived physiological, multimodal, "
            "and alarm-centered temporal measurements after internal "
            "consistency checks, while keeping descriptive observations "
            "separate from scientific validation, alarm credibility, "
            "and clinical decision-making."
        ),

        "validation_state": {
            "relationship_validation": (
                "internal_consistency_passed"
                if validation_passed
                else "internal_consistency_issues_detected"
            ),

            "scientific_validation": "not_established",
            "clinical_validation": "not_established",
        },

        "physiological_reasoning": physiological,

        "multimodal_reasoning": multimodal,

        "temporal_reasoning": temporal,

        "temporal_change_reasoning": temporal_changes,

        "observations": observations,

        "reasoning_summary": {
            "physiological_evidence_available": bool(
                physiological
            ),

            "multimodal_relationship_available": (
                multimodal.get("reasoning_state")
                == "computed_temporal_association_available"
            ),

            "temporal_context_available": bool(temporal),

            "temporal_changes_available": bool(
                temporal_changes
            ),

            "reasoning_state": reasoning_state,
        },

        "limitations": limitations,

        "credibility_assessment": {
            "status": "not_assigned",

            "reason": (
                "The current reasoning layer is descriptive. "
                "No alarm credibility score or validity classification "
                "is assigned."
            ),
        },

        "clinical_decision": None,
    }


def save_reasoning_profile(profile):
    EPISODE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            profile,
            f,
            indent=4,
            allow_nan=False
        )

    print(f"Output: {OUTPUT_FILE}")


def main():
    relationship = load_json(RELATIONSHIP_FILE)
    interpretation = load_json(INTERPRETATION_FILE)
    validation = load_json(INPUT_FILE)

    profile = build_reasoning_profile(
        relationship,
        interpretation,
        validation
    )

    save_reasoning_profile(profile)


if __name__ == "__main__":
    main()
