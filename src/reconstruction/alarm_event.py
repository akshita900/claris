import json
from pathlib import Path


EPISODE_DIR = Path("data/episodes/003c13_0115")

EVIDENCE_PROFILE_FILE = EPISODE_DIR / "evidence_profile.json"
EVIDENCE_REASONING_FILE = EPISODE_DIR / "evidence_reasoning.json"

OUTPUT_FILE = EPISODE_DIR / "alarm_event.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_alarm_event(evidence_profile, evidence_reasoning):
    alarm = evidence_profile["alarm"]
    recording = evidence_profile["recording"]

    event = {
        "episode": evidence_profile["event"],

        "event_metadata": {
            "event_type": "alarm_event",
            "sampling_frequency_hz": recording["sampling_frequency_hz"],
            "alarm_reference_sample": alarm["reference_sample"],
            "alarm_reference_time_seconds": alarm["reference_time_seconds"],
        },

        "signals": {
            "available": list(
                evidence_profile["signal_quality_evidence"].keys()
            )
        },

        "physiological_evidence": (
            evidence_reasoning["physiological_reasoning"]
        ),

        "multimodal_evidence": (
            evidence_reasoning["multimodal_reasoning"]
        ),

        "temporal_evidence": {
            "windows": evidence_reasoning["temporal_reasoning"],
            "changes": evidence_reasoning["temporal_change_reasoning"],
        },

        "observations": evidence_reasoning["observations"],

        "reasoning_summary": evidence_reasoning["reasoning_summary"],

        "clinical_boundary": {
            "credibility_score": None,
            "credibility_status": (
                evidence_reasoning["credibility_assessment"]["status"]
            ),
            "clinical_decision": None,
        },

        "limitations": evidence_reasoning["limitations"],
    }

    return event


def save_alarm_event(event):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(event, f, indent=4)


def main():
    evidence_profile = load_json(EVIDENCE_PROFILE_FILE)
    evidence_reasoning = load_json(EVIDENCE_REASONING_FILE)

    alarm_event = build_alarm_event(
        evidence_profile,
        evidence_reasoning,
    )

    save_alarm_event(alarm_event)

    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()