from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import json


REQUIRED_DIAGNOSTIC_FIELDS = {
    "diagnostic_id": str,
    "category": str,
    "severity": str,
    "title": str,
    "evidence": str,
    "risk": str,
    "recommended_fix": str,
    "patchable": bool,
    "confidence": (int, float),
}

REQUIRED_MANIFEST_FIELDS = {
    "schema_version": str,
    "tool": str,
    "tool_version": str,
    "started_at": str,
    "completed_at": str,
    "target_path": str,
    "output_dir": str,
    "command": list,
    "diagnostics_count": int,
    "outputs": dict,
    "validation_status": str,
}


def validate_diagnostic_record(record: Mapping[str, object]) -> list[str]:
    return _validate_required(record, REQUIRED_DIAGNOSTIC_FIELDS) + _validate_choices(
        record,
        {
            "category": {
                "invocation_clarity",
                "input_output_contract",
                "preconditions",
                "acceptance_criteria",
                "execution_hazards",
                "instruction_conflicts",
                "security_prompt_injection",
                "tool_permission_risk",
                "context_load_discipline",
                "host_adapter_compatibility",
                "verification_gaps",
                "maintainer_handoff",
            },
            "severity": {"info", "minor", "major", "critical"},
        },
    ) + _validate_diagnostic_shapes(record)


def validate_run_manifest(record: Mapping[str, object]) -> list[str]:
    return _validate_required(record, REQUIRED_MANIFEST_FIELDS) + _validate_choices(
        record,
        {
            "validation_status": {"Not Run", "Failed", "Passed", "Partially Verified", "Stale", "Not Applicable"},
        },
    )


def validate_jsonl_file(path: str | Path) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc}")
            continue
        for error in validate_diagnostic_record(record):
            errors.append(f"line {line_number}: {error}")
    return errors


def _validate_required(record: Mapping[str, object], fields: Mapping[str, object]) -> list[str]:
    errors: list[str] = []
    for field_name, expected_type in fields.items():
        if field_name not in record:
            errors.append(f"missing required field: {field_name}")
            continue
        if not isinstance(record[field_name], expected_type):
            errors.append(f"field {field_name} has wrong type")
    return errors


def _validate_choices(record: Mapping[str, object], choices: Mapping[str, set[str]]) -> list[str]:
    errors: list[str] = []
    for field_name, allowed in choices.items():
        if field_name in record and record[field_name] not in allowed:
            errors.append(f"field {field_name} has invalid value: {record[field_name]}")
    return errors


def _validate_diagnostic_shapes(record: Mapping[str, object]) -> list[str]:
    errors: list[str] = []
    diagnostic_id = record.get("diagnostic_id")
    if isinstance(diagnostic_id, str) and not __import__("re").match(r"^SD[0-9]{3}$", diagnostic_id):
        errors.append(f"field diagnostic_id has invalid value: {diagnostic_id}")
    confidence = record.get("confidence")
    if isinstance(confidence, (int, float)) and not 0 <= confidence <= 1:
        errors.append(f"field confidence is outside 0..1: {confidence}")
    return errors
