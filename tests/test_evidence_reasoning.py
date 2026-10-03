
import copy
import json
import math
import unittest
from pathlib import Path

from src.reconstruction.evidence_reasoning import (
    build_reasoning_profile,
    load_json,
)


ROOT = Path(__file__).resolve().parents[1]
EPISODE_DIR = ROOT / "data/episodes/003c13_0115"


class EvidenceReasoningTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.relationship = load_json(
            EPISODE_DIR / "evidence_relationship.json"
        )

        cls.interpretation = load_json(
            EPISODE_DIR / "evidence_interpretation.json"
        )

        cls.validation = load_json(
            EPISODE_DIR / "relationship_validation.json"
        )

    def build_profile(self):
        return build_reasoning_profile(
            copy.deepcopy(self.relationship),
            copy.deepcopy(self.interpretation),
            copy.deepcopy(self.validation),
        )

    def test_internal_validation_does_not_claim_scientific_validity(self):
        profile = self.build_profile()

        self.assertEqual(
            profile["validation_state"]["relationship_validation"],
            "internal_consistency_passed",
        )

        self.assertEqual(
            profile["validation_state"]["scientific_validation"],
            "not_established",
        )

        self.assertEqual(
            profile["validation_state"]["clinical_validation"],
            "not_established",
        )

    def test_clinical_decision_remains_null(self):
        profile = self.build_profile()

        self.assertIsNone(profile["clinical_decision"])

    def test_alarm_credibility_remains_unassigned(self):
        profile = self.build_profile()

        self.assertEqual(
            profile["credibility_assessment"]["status"],
            "not_assigned",
        )

    def test_missing_heart_rate_remains_unavailable(self):
        profile = self.build_profile()

        unavailable_windows = [
            item
            for item in profile["temporal_reasoning"]
            if item["heart_rate_available"] is False
        ]

        self.assertGreater(len(unavailable_windows), 0)

        for item in unavailable_windows:
            self.assertIsNone(item["heart_rate"])

    def test_sparse_window_is_not_a_clinical_conclusion(self):
        profile = self.build_profile()

        for item in profile["temporal_reasoning"]:
            self.assertIn(
                item["reasoning_state"],
                {
                    "relationship_measurement_unavailable",
                    "sparse_relationship_evidence",
                    "relationship_observed_rate_unavailable",
                    "relationship_observed_measurements_available",
                },
            )

    def test_non_finite_values_cannot_be_serialized(self):
        profile = self.build_profile()

        profile["test_value"] = float("nan")

        with self.assertRaises(ValueError):
            json.dumps(profile, allow_nan=False)

    def test_reasoning_output_preserves_episode_identity(self):
        profile = self.build_profile()

        self.assertEqual(
            profile["episode"],
            "003c13_0115",
        )

    def test_reasoning_state_is_descriptive(self):
        profile = self.build_profile()

        self.assertEqual(
            profile["reasoning_summary"]["reasoning_state"],
            "descriptive_evidence_available",
        )


if __name__ == "__main__":
    unittest.main()
