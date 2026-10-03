
import copy
import json
import math
import unittest
from pathlib import Path

from src.reconstruction.relationship_validation import (
    build_validation_profile,
    load_json,
)


ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data/episodes/003c13_0115/evidence_relationship.json"


class RelationshipValidationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.valid_data = load_json(INPUT_FILE)

    def validate(self, data):
        return build_validation_profile(data)

    def failed_checks(self, data):
        profile = self.validate(data)
        return [
            check["check"]
            for check in profile["checks"]
            if not check["passed"]
        ]

    def test_existing_episode(self):
        profile = self.validate(copy.deepcopy(self.valid_data))

        self.assertEqual(profile["validation_summary"]["total_checks"], 6)
        self.assertEqual(profile["validation_summary"]["failed_checks"], 0)

    def test_negative_event_count_rejected(self):
        data = copy.deepcopy(self.valid_data)
        data["physiological_evidence"][0]["event_count"] = -1

        self.assertIn(
            "physiological_event_counts",
            self.failed_checks(data)
        )

    def test_boolean_event_count_rejected(self):
        data = copy.deepcopy(self.valid_data)
        data["physiological_evidence"][0]["event_count"] = True

        self.assertIn(
            "physiological_event_counts",
            self.failed_checks(data)
        )

    def test_fractional_event_count_rejected(self):
        data = copy.deepcopy(self.valid_data)
        data["physiological_evidence"][0]["event_count"] = 3.5

        self.assertIn(
            "physiological_event_counts",
            self.failed_checks(data)
        )

    def test_nan_rate_rejected(self):
        data = copy.deepcopy(self.valid_data)
        data["physiological_evidence"][0]["mean_heart_rate_bpm"] = math.nan

        self.assertIn(
            "physiological_event_counts",
            self.failed_checks(data)
        )

    def test_matching_fraction_above_one_rejected(self):
        data = copy.deepcopy(self.valid_data)
        data["multimodal_relationship"]["alarm_window_relationship"][
            "matching_fraction"
        ] = 1.5

        self.assertIn(
            "multimodal_relationship_consistency",
            self.failed_checks(data)
        )

    def test_temporal_matched_count_cannot_exceed_pleth(self):
        data = copy.deepcopy(self.valid_data)
        data["temporal_relationships"][0]["matched_events"] = 10

        self.assertIn(
            "temporal_relationship_consistency",
            self.failed_checks(data)
        )

    def test_inconsistent_temporal_change_rejected(self):
        data = copy.deepcopy(self.valid_data)
        data["temporal_changes"][0]["ecg_event_change"] = 99

        self.assertIn(
            "temporal_change_consistency",
            self.failed_checks(data)
        )

    def test_clinical_boundary_preserved(self):
        profile = self.validate(copy.deepcopy(self.valid_data))

        self.assertIsNone(profile["credibility_score"])
        self.assertIsNone(profile["clinical_decision"])

    def test_non_null_clinical_decision_rejected(self):
        data = copy.deepcopy(self.valid_data)
        data["clinical_decision"] = "some decision"

        self.assertIn(
            "clinical_boundary_preserved",
            self.failed_checks(data)
        )


if __name__ == "__main__":
    unittest.main()
