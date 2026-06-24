from __future__ import annotations

import json
from pathlib import Path

from .diagnostics import DiagnosticRecord


def write_outputs(
    *,
    out_dir: Path,
    target: Path,
    diagnostics: list[DiagnosticRecord],
    manifest: dict[str, object],
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    output_paths = {
        "diagnostics_jsonl": out_dir / "diagnostics.jsonl",
        "skill_report": out_dir / "skill_report.md",
        "remediation_tasks": out_dir / "remediation_tasks.md",
        "suggested_patch": out_dir / "suggested_patch.md",
        "run_manifest": out_dir / "run_manifest.json",
    }

    _write_jsonl(output_paths["diagnostics_jsonl"], diagnostics)
    output_paths["skill_report"].write_text(_render_report(target, diagnostics), encoding="utf-8")
    output_paths["remediation_tasks"].write_text(_render_tasks(diagnostics), encoding="utf-8")
    output_paths["suggested_patch"].write_text(_render_patch_suggestions(diagnostics), encoding="utf-8")
    output_paths["run_manifest"].write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return output_paths


def _write_jsonl(path: Path, diagnostics: list[DiagnosticRecord]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for diagnostic in diagnostics:
            handle.write(json.dumps(diagnostic.to_dict(), sort_keys=True) + "\n")


def _render_report(target: Path, diagnostics: list[DiagnosticRecord]) -> str:
    lines = [
        "# SkillDoctor Report",
        "",
        f"Target: `{target}`",
        "",
        f"Diagnostics: {len(diagnostics)}",
        "",
    ]
    if not diagnostics:
        lines.extend(["No diagnostics were produced by the v0.1 deterministic checks.", ""])
        return "\n".join(lines)

    for diagnostic in diagnostics:
        lines.extend(
            [
                f"## {diagnostic.diagnostic_id}: {diagnostic.title}",
                "",
                f"- Category: `{diagnostic.category}`",
                f"- Severity: `{diagnostic.severity}`",
                f"- Confidence: `{diagnostic.confidence:.2f}`",
                f"- Patchable: `{str(diagnostic.patchable).lower()}`",
                f"- Evidence: {diagnostic.evidence}",
                f"- Risk: {diagnostic.risk}",
                f"- Recommended fix: {diagnostic.recommended_fix}",
                "",
            ]
        )
    return "\n".join(lines)


def _render_tasks(diagnostics: list[DiagnosticRecord]) -> str:
    lines = ["# Remediation Tasks", ""]
    if not diagnostics:
        lines.extend(["- [x] No remediation tasks produced by current checks.", ""])
        return "\n".join(lines)

    for diagnostic in diagnostics:
        lines.append(f"- [ ] {diagnostic.diagnostic_id} ({diagnostic.severity}): {diagnostic.recommended_fix}")
    lines.append("")
    return "\n".join(lines)


def _render_patch_suggestions(diagnostics: list[DiagnosticRecord]) -> str:
    lines = [
        "# Suggested Patch",
        "",
        "SkillDoctor v0.1 does not apply changes automatically. Use these conservative suggestions as review input.",
        "",
    ]
    patchable = [diagnostic for diagnostic in diagnostics if diagnostic.patchable]
    if not patchable:
        lines.extend(["No patchable diagnostics were produced.", ""])
        return "\n".join(lines)

    for diagnostic in patchable:
        lines.extend(
            [
                f"## {diagnostic.diagnostic_id}: {diagnostic.title}",
                "",
                f"Suggested edit: {diagnostic.recommended_fix}",
                "",
            ]
        )
    return "\n".join(lines)

