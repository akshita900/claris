from pathlib import Path
import json


# ============================================================
# CLARIS - Evidence Fusion
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODE_DIR = (
    PROJECT_ROOT
    / "data"
    / "episodes"
    / "003c13_0115"
)

INPUT_FILE = (
    EPISODE_DIR
    / "evidence_interpretation.json"
)

OUTPUT_FILE = (
    EPISODE_DIR
    / "evidence_fusion.json"
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
# Evidence Pattern
# ============================================================

def determine_evidence_pattern(
    interpretation
):

    multimodal = interpretation.get(
        "multimodal_evidence",
        {}
    )

    temporal = interpretation.get(
        "temporal_context",
        {}
    )

    physiological = interpretation.get(
        "physiological_evidence",
        []
    )

    multimodal_state = multimodal.get(
        "state"
    )

    temporal_windows = temporal.get(
        "windows",
        []
    )

    physiological_available = any(
        item.get("state") == "available"
        for item in physiological
    )

    temporal_available = any(
        item.get("state") == "context_observed"
        for item in temporal_windows
    )

    if (
        multimodal_state == "relationship_observed"
        and temporal_available
    ):

        return "multimodal_context_available"

    if multimodal_state == "relationship_observed":

        return "multimodal_relationship_available"

    if (
        physiological_available
        and temporal_available
    ):

        return "physiological_context_available"

    if physiological_available:

        return "physiological_evidence_available"

    return "insufficient_evidence"


# ============================================================
# Supporting Components
# ============================================================

def identify_components(
    interpretation
):

    supporting = []
    partial = []
    insufficient = []
    inconsistent = []

    # --------------------------------------------------------
    # Physiological evidence
    # --------------------------------------------------------

    physiological = interpretation.get(
        "physiological_evidence",
        []
    )

    if any(
        item.get("state") == "available"
        for item in physiological
    ):

        supporting.append(
            "physiological_evidence"
        )

    else:

        insufficient.append(
            "physiological_evidence"
        )

    # --------------------------------------------------------
    # Multimodal evidence
    # --------------------------------------------------------

    multimodal = interpretation.get(
        "multimodal_evidence",
        {}
    )

    multimodal_state = multimodal.get(
        "state"
    )

    if multimodal_state == "relationship_observed":

        supporting.append(
            "multimodal_evidence"
        )

    elif multimodal_state == "insufficient_evidence":

        insufficient.append(
            "multimodal_evidence"
        )

    # --------------------------------------------------------
    # Temporal context
    # --------------------------------------------------------

    temporal = interpretation.get(
        "temporal_context",
        {}
    )

    temporal_windows = temporal.get(
        "windows",
        []
    )

    if any(
        item.get("state") == "context_observed"
        for item in temporal_windows
    ):

        supporting.append(
            "temporal_context"
        )

    else:

        insufficient.append(
            "temporal_context"
        )

    return (
        supporting,
        partial,
        insufficient,
        inconsistent
    )


# ============================================================
# Main
# ============================================================

def main():

    interpretation = load_json(
        INPUT_FILE
    )

    (
        supporting,
        partial,
        insufficient,
        inconsistent
    ) = identify_components(
        interpretation
    )

    evidence_pattern = (
        determine_evidence_pattern(
            interpretation
        )
    )

    output = {

        "episode":
            interpretation.get(
                "episode"
            ),

        "purpose":
            (
                "Combine independently measured "
                "evidence streams into a structured "
                "evidence pattern while preserving "
                "the identity and limitations of each "
                "evidence source."
            ),

        "evidence_pattern":
            evidence_pattern,

        "evidence_components": {

            "signal_quality":
                interpretation.get(
                    "signal_quality",
                    []
                ),

            "physiological_evidence":
                interpretation.get(
                    "physiological_evidence",
                    []
                ),

            "multimodal_evidence":
                interpretation.get(
                    "multimodal_evidence",
                    {}
                ),

            "temporal_context":
                interpretation.get(
                    "temporal_context",
                    {}
                )
        },

        "evidence_summary": {

            "supporting_components":
                supporting,

            "partially_supported_components":
                partial,

            "insufficient_components":
                insufficient,

            "inconsistent_components":
                inconsistent
        },

        "interpretation": {

            "evidence_is_multimodal":
                (
                    interpretation
                    .get(
                        "multimodal_evidence",
                        {}
                    )
                    .get(
                        "state"
                    )
                    == "relationship_observed"
                ),

            "temporal_context_available":
                len(
                    [
                        item
                        for item in
                        interpretation
                        .get(
                            "temporal_context",
                            {}
                        )
                        .get(
                            "windows",
                            []
                        )
                        if item.get(
                            "state"
                        )
                        == "context_observed"
                    ]
                ) > 0,

            "physiological_evidence_available":
                len(
                    [
                        item
                        for item in
                        interpretation
                        .get(
                            "physiological_evidence",
                            []
                        )
                        if item.get(
                            "state"
                        )
                        == "available"
                    ]
                ) > 0,

            "multimodal_relationship_available":
                (
                    interpretation
                    .get(
                        "multimodal_evidence",
                        {}
                    )
                    .get(
                        "state"
                    )
                    == "relationship_observed"
                ),

            "evidence_limitations": [

                "Sparse temporal windows may not support rate estimation.",

                "Measured ECG-PPG relationships describe temporal association only.",

                "The observed evidence does not establish alarm validity.",

                "No clinical diagnosis is inferred.",

                "No alarm credibility score is assigned."
            ]
        },

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
        "Evidence fusion generated."
    )

    print(
        f"Evidence pattern: {evidence_pattern}"
    )

    print(
        f"Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    main()