import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
EPISODE = "003c13_0115"
SOURCE_DIR = ROOT / "data" / "episodes" / EPISODE
AUDIT_SCRIPT = ROOT / "src" / "reconstruction" / "evidence_audit.py"

FILES = [
    "alarm_event.json",
    "evidence_reasoning.json",
    "evidence_relationship.json",
    "multimodal_evidence.json",
    "evidence_reliability.json",
    "metadata.json",
    "episode_validation.json",
]

print("CLARIS - Controlled Audit Sensitivity Test")
print("------------------------------------------")

if not AUDIT_SCRIPT.exists():
    raise FileNotFoundError(AUDIT_SCRIPT)

with tempfile.TemporaryDirectory(prefix="claris_audit_test_") as temp:
    temp_root = Path(temp)
    test_episode = temp_root / "data" / "episodes" / EPISODE
    test_episode.mkdir(parents=True)

    for filename in FILES:
        source = SOURCE_DIR / filename

        if not source.exists():
            raise FileNotFoundError(
                f"Required source file missing: {source}"
            )

        shutil.copy2(source, test_episode / filename)

    alarm_path = test_episode / "alarm_event.json"

    with open(alarm_path, "r", encoding="utf-8") as file:
        alarm = json.load(file)

    physiological = alarm.get("physiological_evidence")

    if not isinstance(physiological, list) or not physiological:
        raise RuntimeError(
            "Physiological evidence unavailable; test aborted."
        )

    target = next(
        (
            item for item in physiological
            if isinstance(item, dict)
            and isinstance(item.get("observations"), dict)
            and item["observations"]
        ),
        None
    )

    if target is None:
        raise RuntimeError(
            "No suitable physiological measurement found."
        )

    observations = target["observations"]

    numeric_field = next(
        (
            key for key, value in observations.items()
            if isinstance(value, (int, float))
            and not isinstance(value, bool)
        ),
        None
    )

    if numeric_field is None:
        raise RuntimeError(
            "No numeric physiological measurement found."
        )

    original_value = observations[numeric_field]
    observations[numeric_field] = original_value + 12345

    with open(alarm_path, "w", encoding="utf-8") as file:
        json.dump(alarm, file, indent=4, allow_nan=False)

    # Run the existing audit implementation against temporary data.
    audit_copy = temp_root / "evidence_audit.py"
    shutil.copy2(AUDIT_SCRIPT, audit_copy)

    result = subprocess.run(
        [sys.executable, str(audit_copy)],
        cwd=temp_root,
        capture_output=True,
        text=True
    )

    print(f"Altered signal: {target.get('signal')}")
    print(f"Altered field: {numeric_field}")
    print(f"Original value: {original_value}")
    print(f"Test value: {observations[numeric_field]}")
    print()

    if result.returncode != 0:
        print("AUDIT EXECUTION FAILED")
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(result.returncode)

    report_path = test_episode / "evidence_audit.json"

    if not report_path.exists():
        raise RuntimeError("Temporary audit report was not generated.")

    with open(report_path, "r", encoding="utf-8") as file:
        report = json.load(file)

    findings = report.get("findings", [])

    traceability = next(
        (
            item for item in findings
            if item.get("check") == "physiological_evidence_traceability"
        ),
        None
    )

    if traceability is None:
        print("TEST INCONCLUSIVE: traceability finding missing.")
    elif traceability.get("status") == "warning":
        print("PASS: Audit detected the deliberately altered measurement.")
        print(traceability.get("detail"))
    else:
        print("FAIL: Audit did not flag the altered measurement.")
        print(traceability)

    print()
    print("Temporary test directory will be removed automatically.")
    print("Original CLARIS episode files were not used as write targets.")
    print("Original audit report was not overwritten.")
