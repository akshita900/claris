from pathlib import Path
import json


# ============================================================
# CLARIS - Evidence Relationship / Temporal Reasoning
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODE_DIR = (
    PROJECT_ROOT
    / "data"
    / "episodes"
    / "003c13_0115"
)

INTERPRETATION_FILE = (
    EPISODE_DIR
    / "evidence_interpretation.json"
)

OUTPUT_FILE = (
    EPISODE_DIR
    / "evidence_relationship.json"
)


# ============================================================
# Load JSON
# ============================================================

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# Temporal Relationship
# ============================================================

def analyze_temporal_relationship(
    temporal_context
):

    windows = temporal_context.get(
        "windows",
        []
    )

    relationships = []

    for window in windows:

        relationships.append({

            "window":
                window.get(
                    "window"
                ),

            "ecg_events":
                window.get(
                    "ecg_events"
                ),

            "pleth_events":
                window.get(
                    "pleth_events"
                ),

            "matched_events":
                window.get(
                    "matched_events"
                ),

            "matching_fraction":
                window.get(
                    "matching_fraction"
                ),

            "ecg_pleth_delay_seconds":
                window.get(
                    "mean_delay_seconds"
                ),

            "heart_rate":
                window.get(
                    "heart_rate"
                ),

            "heart_rate_available":
                window.get(
                    "heart_rate_available"
                ),

            "relationship_state":
                (
                    "relationship_observed"
                    if window.get(
                        "matched_events"
                    ) is not None
                    and window.get(
                        "matched_events"
                    ) > 0
                    else
                    "insufficient_evidence"
                )
        })

    return relationships


# ============================================================
# Temporal Change
# ============================================================

def analyze_temporal_changes(
    temporal_context
):

    changes = temporal_context.get(
        "temporal_changes",
        {}
    )

    interpreted_changes = []

    for transition, change in changes.items():

        interpreted_changes.append({

            "transition":
                transition,

            "ecg_event_change":
                change.get(
                    "ecg_peak_count"
                ),

            "pleth_event_change":
                change.get(
                    "pleth_pulse_count"
                ),

            "matching_fraction_change":
                change.get(
                    "matching_fraction"
                ),

            "ecg_pleth_delay_change_seconds":
                change.get(
                    "ecg_pleth_delay_mean_seconds"
                ),

            "rr_variability_change_seconds":
                change.get(
                    "rr_std_seconds"
                ),

            "heart_rate_change_bpm":
                change.get(
                    "mean_heart_rate_bpm"
                )
        })

    return interpreted_changes


# ============================================================
# Multimodal Relationship
# ============================================================

def analyze_multimodal_relationship(
    multimodal
):

    global_data = multimodal.get(
        "global",
        {}
    )

    alarm_data = multimodal.get(
        "alarm_window",
        {}
    )

    return {

        "signals_used":
            multimodal.get(
                "signals_used",
                {}
            ),

        "global_relationship": {

            "matched_events":
                global_data.get(
                    "matched_event_count"
                ),

            "mean_delay_seconds":
                global_data.get(
                    "mean_delay_seconds"
                )
        },

        "alarm_window_relationship": {

            "ecg_events":
                alarm_data.get(
                    "ecg_event_count"
                ),

            "matched_events":
                alarm_data.get(
                    "matched_event_count"
                ),

            "matching_fraction":
                alarm_data.get(
                    "matching_fraction"
                ),

            "mean_delay_seconds":
                alarm_data.get(
                    "mean_delay_seconds"
                ),

            "delay_std_seconds":
                alarm_data.get(
                    "delay_std_seconds"
                )
        },

        "relationship_state":
            multimodal.get(
                "state"
            )
    }


# ============================================================
# Physiological Relationship
# ============================================================

def analyze_physiological_evidence(
    physiological
):

    relationships = []

    for signal in physiological:

        relationships.append({

            "signal":
                signal.get(
                    "signal"
                ),

            "modality":
                signal.get(
                    "modality"
                ),

            "event_count":
                signal.get(
                    "event_count"
                ),

            "local_event_count":
                signal.get(
                    "local_event_count"
                ),

            "mean_heart_rate_bpm":
                signal.get(
                    "mean_heart_rate_bpm"
                ),

            "mean_pulse_rate_bpm":
                signal.get(
                    "mean_pulse_rate_bpm"
                )
        })

    return relationships


# ============================================================
# Build Relationship Profile
# ============================================================

def build_relationship_profile(
    interpretation
):

    temporal_context = interpretation.get(
        "temporal_context",
        {}
    )

    multimodal = interpretation.get(
        "multimodal_evidence",
        {}
    )

    physiological = interpretation.get(
        "physiological_evidence",
        []
    )

    temporal_relationships = (
        analyze_temporal_relationship(
            temporal_context
        )
    )

    temporal_changes = (
        analyze_temporal_changes(
            temporal_context
        )
    )

    multimodal_relationship = (
        analyze_multimodal_relationship(
            multimodal
        )
    )

    physiological_relationship = (
        analyze_physiological_evidence(
            physiological
        )
    )

    return {

        "episode":
            interpretation.get(
                "episode"
            ),

        "purpose":
            (
                "Describe relationships and temporal "
                "changes between independently measured "
                "physiological evidence streams without "
                "assigning alarm credibility or making "
                "a clinical decision."
            ),

        "physiological_evidence":
            physiological_relationship,

        "multimodal_relationship":
            multimodal_relationship,

        "temporal_relationships":
            temporal_relationships,

        "temporal_changes":
            temporal_changes,

        "relationship_summary": {

            "multimodal_relationship_observed":
                (
                    multimodal.get(
                        "state"
                    )
                    == "relationship_observed"
                ),

            "temporal_context_observed":
                len(
                    temporal_relationships
                ) > 0,

            "temporal_changes_available":
                len(
                    temporal_changes
                ) > 0
        },

        "limitations": [

            "Temporal association does not establish causation.",

            "Detected events represent signal-derived measurements and not clinical diagnoses.",

            "Sparse temporal windows may limit rate estimation.",

            "The observed relationships do not establish alarm validity.",

            "No alarm credibility score is assigned.",

            "No clinical decision is generated."
        ],

        "credibility_score":
            None,

        "clinical_decision":
            None
    }


# ============================================================
# Save
# ============================================================

def save_relationship_profile(
    profile
):

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            profile,
            file,
            indent=4
        )


# ============================================================
# Main
# ============================================================

def main():

    interpretation = load_json(
        INTERPRETATION_FILE
    )

    profile = build_relationship_profile(
        interpretation
    )

    save_relationship_profile(
        profile
    )

    print(
        "Evidence relationship analysis generated."
    )

    print(
        f"Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    main()