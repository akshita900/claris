from pathlib import Path
import json


# ============================================================
# CLARIS - Alarm Evidence Profile
# Phase 2
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODE_DIR = PROJECT_ROOT / "data" / "episodes"


# ============================================================
# Load JSON helper
# ============================================================

def load_json(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# ============================================================
# Build evidence profile
# ============================================================

def build_evidence_profile(
    event_name
):
    """
    Combine previously generated CLARIS evidence
    into one structured alarm-level profile.

    This function does NOT assign a clinical
    credibility score.
    """

    episode_path = (
        EPISODE_DIR / event_name
    )

    metadata = load_json(
        episode_path / "metadata.json"
    )

    signal_quality = load_json(
        episode_path / "signal_quality.json"
    )

    physiological = load_json(
        episode_path / "physiological_features.json"
    )

    multimodal = load_json(
        episode_path / "multimodal_evidence.json"
    )

    alarm_context = load_json(
        episode_path / "alarm_context.json"
    )

    # --------------------------------------------------------
    # Basic event information
    # --------------------------------------------------------

    profile = {

        "event": event_name,

        "recording": {

            "sampling_frequency_hz":
                metadata[
                    "sampling_frequency_hz"
                ],

            "total_samples":
                metadata[
                    "total_samples"
                ],

            "signals":
                metadata[
                    "signals"
                ]
        },

        "alarm": {

            "reference_sample":
                metadata[
                    "event_window"
                ][
                    "alarm_reference_sample"
                ],

            "reference_time_seconds":
                metadata[
                    "event_window"
                ][
                    "alarm_reference_time_seconds"
                ]
        },

        # ----------------------------------------------------
        # Signal quality evidence
        # ----------------------------------------------------

        "signal_quality_evidence": {},

        # ----------------------------------------------------
        # Physiological evidence
        # ----------------------------------------------------

        "physiological_evidence": {},

        # ----------------------------------------------------
        # Multimodal evidence
        # ----------------------------------------------------

        "multimodal_evidence": {},

        # ----------------------------------------------------
        # Temporal context
        # ----------------------------------------------------

        "temporal_context": {},

        # ----------------------------------------------------
        # Evidence availability
        # ----------------------------------------------------

        "evidence_availability": {}
    }

    # ========================================================
    # Signal quality
    # ========================================================

    for signal_name, result in signal_quality.items():

        profile[
            "signal_quality_evidence"
        ][signal_name] = {

            "modality":
                result["modality"],

            "features":
                result["features"]
        }

    # ========================================================
    # Physiological evidence
    # ========================================================

    for signal_name, result in physiological.items():

        profile[
            "physiological_evidence"
        ][signal_name] = {

            "modality":
                result["modality"],

            "features":
                result["features"]
        }

    # ========================================================
    # Multimodal evidence
    # ========================================================

    profile[
        "multimodal_evidence"
    ] = {

        "signals_used":
            multimodal.get(
                "signals_used",
                {
                    "ecg": "II",
                    "pleth": "PLETH"
                }
            ),

        "global":
            multimodal.get(
                "global",
                {}
            ),

        "alarm_window":
            multimodal.get(
                "alarm_window",
                {}
            )
    }

    # ========================================================
    # Temporal context
    # ========================================================

    profile[
        "temporal_context"
    ] = {

        "windows":
            alarm_context.get(
                "windows",
                {}
            ),

        "temporal_changes":
            alarm_context.get(
                "temporal_changes",
                {}
            )
    }

    # ========================================================
    # Evidence availability
    # ========================================================

    for signal_name, result in physiological.items():

        features = result.get(
            "features",
            {}
        )

        available = {}

        for feature_name, value in features.items():

            if value is None:

                available[
                    feature_name
                ] = False

            else:

                available[
                    feature_name
                ] = True

        profile[
            "evidence_availability"
        ][signal_name] = available

    return profile


# ============================================================
# Save profile
# ============================================================

def save_profile(
    event_name,
    profile
):

    episode_path = (
        EPISODE_DIR / event_name
    )

    output_path = (
        episode_path /
        "evidence_profile.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            profile,
            file,
            indent=4
        )

    return output_path


# ============================================================
# Print summary
# ============================================================

def print_summary(
    profile,
    output_path
):

    print()
    print("=" * 40)
    print("CLARIS - Alarm Evidence Profile")
    print("=" * 40)

    print(
        f"Event: "
        f"{profile['event']}"
    )

    print()
    print("----------------------------------------")
    print("ALARM")
    print("----------------------------------------")

    print(
        "Reference time: "
        f"{profile['alarm']['reference_time_seconds']:.3f} s"
    )

    print()
    print("----------------------------------------")
    print("SIGNALS")
    print("----------------------------------------")

    for signal_name, signal_info in (
        profile[
            "recording"
        ][
            "signals"
        ].items()
    ):

        print(
            f"  {signal_name} -> "
            f"{signal_info['modality']}"
        )

    print()
    print("----------------------------------------")
    print("SIGNAL QUALITY EVIDENCE")
    print("----------------------------------------")

    for signal_name in (
        profile[
            "signal_quality_evidence"
        ]
    ):

        print(
            f"  {signal_name}: "
            "features available"
        )

    print()
    print("----------------------------------------")
    print("PHYSIOLOGICAL EVIDENCE")
    print("----------------------------------------")

    for signal_name, result in (
        profile[
            "physiological_evidence"
        ].items()
    ):

        features = result[
            "features"
        ]

        print(
            f"\n  {signal_name}"
        )

        if "peak_count" in features:

            print(
                f"    Events detected: "
                f"{features['peak_count']}"
            )

        if "local_peak_count" in features:

            print(
                f"    Local events: "
                f"{features['local_peak_count']}"
            )

        if "mean_heart_rate_bpm" in features:

            print(
                f"    Mean heart rate: "
                f"{features['mean_heart_rate_bpm']}"
            )

        if "mean_pulse_rate_bpm" in features:

            print(
                f"    Mean pulse rate: "
                f"{features['mean_pulse_rate_bpm']}"
            )

    print()
    print("----------------------------------------")
    print("MULTIMODAL EVIDENCE")
    print("----------------------------------------")

    multimodal = profile[
        "multimodal_evidence"
    ]

    global_data = multimodal[
        "global"
    ]

    alarm_data = multimodal[
        "alarm_window"
    ]

    print(
        f"  Global ECG-PLETH matches: "
        f"{global_data.get('matched_event_count')}"
    )

    print(
        f"  Global mean delay: "
        f"{global_data.get('mean_ecg_pleth_delay_seconds')}"
    )

    print(
        f"  Alarm-window matches: "
        f"{alarm_data.get('matched_beat_count')}"
    )

    print(
        f"  Alarm-window matching fraction: "
        f"{alarm_data.get('matching_fraction')}"
    )

    print(
        f"  Alarm-window mean delay: "
        f"{alarm_data.get('ecg_pleth_delay_mean_seconds')}"
    )

    print()
    print("----------------------------------------")
    print("TEMPORAL CONTEXT")
    print("----------------------------------------")

    for window_name, window in (
        profile[
            "temporal_context"
        ][
            "windows"
        ].items()
    ):

        print(
            f"\n  {window_name}"
        )

        print(
            f"    ECG events: "
            f"{window['ecg_peak_count']}"
        )

        print(
            f"    PLETH events: "
            f"{window['pleth_pulse_count']}"
        )

        print(
            f"    Matched events: "
            f"{window['matched_event_count']}"
        )

        print(
            f"    Matching fraction: "
            f"{window['matching_fraction']:.3f}"
        )

        print(
            f"    HR available: "
            f"{window['heart_rate_available']}"
        )

    print()
    print("----------------------------------------")
    print("EVIDENCE PROFILE")
    print("----------------------------------------")

    print(
        "The profile combines measurable evidence "
        "without assigning a clinical credibility "
        "score."
    )

    print()
    print("----------------------------------------")
    print("Saved to:")
    print(output_path)
    print("----------------------------------------")

    print()
    print("=" * 40)
    print("Alarm evidence profile complete.")
    print("=" * 40)


# ============================================================
# Main
# ============================================================

def main():

    event_name = "003c13_0115"

    profile = build_evidence_profile(
        event_name
    )

    output_path = save_profile(
        event_name,
        profile
    )

    print_summary(
        profile,
        output_path
    )


if __name__ == "__main__":
    main()