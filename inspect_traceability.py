import json
from pathlib import Path

episode_dir = Path("data/episodes/003c13_0115")

files = [
    "alarm_context.json",
    "physiological_features.json",
    "multimodal_evidence.json",
    "evidence_relationship.json",
    "evidence_interpretation.json",
    "relationship_validation.json",
    "evidence_reasoning.json",
]

for filename in files:
    path = episode_dir / filename
    data = json.loads(path.read_text(encoding="utf-8"))

    print(f"\n--- {filename} ---")

    if filename == "alarm_context.json":
        print(json.dumps({
            "physiological_evidence": data.get("physiological_evidence"),
            "multimodal_evidence": data.get("multimodal_evidence"),
            "temporal_evidence": data.get("temporal_evidence"),
        }, indent=2, ensure_ascii=False))

    elif filename == "physiological_features.json":
        print(json.dumps(data, indent=2, ensure_ascii=False))

    elif filename == "multimodal_evidence.json":
        print(json.dumps(data, indent=2, ensure_ascii=False))

    elif filename == "evidence_relationship.json":
        print(json.dumps(data, indent=2, ensure_ascii=False))

    elif filename == "evidence_interpretation.json":
        print(json.dumps(data, indent=2, ensure_ascii=False))

    elif filename == "relationship_validation.json":
        print(json.dumps(data, indent=2, ensure_ascii=False))

    elif filename == "evidence_reasoning.json":
        print(json.dumps({
            "physiological_reasoning": data.get("physiological_reasoning"),
            "multimodal_reasoning": data.get("multimodal_reasoning"),
            "temporal_reasoning": data.get("temporal_reasoning"),
        }, indent=2, ensure_ascii=False))
