import json
from pathlib import Path

from skill_doctor.audit import run_audit
from skill_doctor.schemas import validate_diagnostic_record, validate_jsonl_file, validate_run_manifest


def test_schema_files_are_valid_json():
    for path in [
        Path("schemas/diagnostic_record.schema.json"),
        Path("schemas/run_manifest.schema.json"),
    ]:
        json.loads(path.read_text(encoding="utf-8"))


def test_generated_outputs_validate_with_local_validators(tmp_path):
    target = Path("examples/bad-skill/SKILL.md")
    out_dir = tmp_path / "run"
    run_audit(target, out_dir, command=["skill-doctor", "audit", str(target), "--out", str(out_dir)])

    assert validate_jsonl_file(out_dir / "diagnostics.jsonl") == []

    manifest = json.loads((out_dir / "run_manifest.json").read_text(encoding="utf-8"))
    assert validate_run_manifest(manifest) == []

    first_record = json.loads((out_dir / "diagnostics.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert validate_diagnostic_record(first_record) == []

