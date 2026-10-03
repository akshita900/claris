from pathlib import Path
import json


# ============================================================
# CLARIS - Evidence Interpretation
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODE_DIR = (
    PROJECT_ROOT
    / "data"
    / "episodes"
    / "003c13_0115"
)

PROFILE_FILE = EPISODE_DIR / "evidence_profile.json"
OUTPUT_FILE = EPISODE_DIR / "evidence_interpretation.json"


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
# Signal Quality
# ============================================================

def interpret_signal_quality(signal_quality):

    interpreted = []

    for signal_name, result in signal_quality.items():

        interpreted.append({

            "signal": signal_name,

            "state": "observed",

            "features_available": True,

            "modality": result.get(
                "modality"
            ),

            "features": result.get(
                "features",
                {}
            )
        })

    return interpreted


# ============================================================
# Physiological Evidence
# ============================================================

def interpret_physiological_evidence(
    physiological
):

    interpreted = []

    for signal_name, result in physiological.items():

        features = result.get(
            "features",
            {}
        )

        heart_rate = features.get(
            "mean_heart_rate_bpm"
        )

        pulse_rate = features.get(
            "mean_pulse_rate_bpm"
        )

        interpreted.append({

            "signal": signal_name,

            "state": "available",

            "modality": result.get(
                "modality"
            ),

            "event_count": features.get(
                "peak_count"
            ),

            "local_event_count": features.get(
                "local_peak_count"
            ),

            "mean_heart_rate_bpm":
                heart_rate,

            "mean_pulse_rate_bpm":
                pulse_rate,

            "rate_available": (
                heart_rate is not None
                or
                pulse_rate is not None
            )
        })

    return interpreted


# ============================================================
# Multimodal Evidence
# ============================================================

def interpret_multimodal_evidence(
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

    matching_fraction = alarm_data.get(
        "matching_fraction"
    )

    if matching_fraction is None:

        state = "insufficient_evidence"

    else:

        state = "relationship_observed"

    return {

        "state": state,

        "signals_used": multimodal.get(
            "signals_used",
            {}
        ),

        "global": {

            "matched_event_count":
                global_data.get(
                    "matched_event_count"
                ),

            "mean_delay_seconds":
                global_data.get(
                    "mean_ecg_pleth_delay_seconds"
                )
        },

        "alarm_window": {

            "ecg_event_count":
                alarm_data.get(
                    "ecg_peak_count"
                ),

            "pleth_event_count":
                alarm_data.get(
                    "pleth_pulse_count"
                ),

            "matched_event_count":
                alarm_data.get(
                    "matched_beat_count"
                ),

            "matching_fraction":
                matching_fraction,

            "mean_delay_seconds":
                alarm_data.get(
                    "ecg_pleth_delay_mean_seconds"
                ),

            "delay_std_seconds":
                alarm_data.get(
                    "ecg_pleth_delay_std_seconds"
                )
        }
    }


# ============================================================
# Temporal Context
# ============================================================

def interpret_temporal_context(
    temporal_context
):

    interpreted_windows = []

    windows = temporal_context.get(
        "windows",
        {}
    )

    for window_name, window in windows.items():

        matched_events = window.get(
            "matched_event_count"
        )

        if matched_events is None:

            state = "insufficient_evidence"

        elif matched_events > 0:

            state = "context_observed"

        else:

            state = "insufficient_evidence"

        interpreted_windows.append({

            "window": window_name,

            "state": state,

            "ecg_events":
                window.get(
                    "ecg_peak_count"
                ),

            "pleth_events":
                window.get(
                    "pleth_pulse_count"
                ),

            "matched_events":
                matched_events,

            "matching_fraction":
                window.get(
                    "matching_fraction"
                ),

            "mean_delay_seconds":
                window.get(
                    "ecg_pleth_delay_mean_seconds"
                ),

            "heart_rate":
                window.get(
                    "mean_heart_rate_bpm"
                ),

            "heart_rate_available":
                window.get(
                    "heart_rate_available"
                )
        })

    temporal_changes = temporal_context.get(
        "temporal_changes",
        {}
    )

    return {

        "windows":
            interpreted_windows,

        "temporal_changes":
            temporal_changes
    }


# ============================================================
# Main
# ============================================================

def main():

    profile = load_json(
        PROFILE_FILE
    )

    output = {

        "episode":
            profile.get(
                "event"
            ),

        "purpose":
            (
                "Translate measured evidence into "
                "structured evidence states without "
                "assigning a clinical credibility score."
            ),

        "signal_quality":
            interpret_signal_quality(
                profile.get(
                    "signal_quality_evidence",
                    {}
                )
            ),

        "physiological_evidence":
            interpret_physiological_evidence(
                profile.get(
                    "physiological_evidence",
                    {}
                )
            ),

        "multimodal_evidence":
            interpret_multimodal_evidence(
                profile.get(
                    "multimodal_evidence",
                    {}
                )
            ),

        "temporal_context":
            interpret_temporal_context(
                profile.get(
                    "temporal_context",
                    {}
                )
            ),

        "credibility_score":
            None,

        "clinical_decision":
            None
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4
        )

    print(
        "Evidence interpretation generated."
    )

    print(
        f"Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    main()