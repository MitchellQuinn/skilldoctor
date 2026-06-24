from __future__ import annotations

from pathlib import Path

from .diagnostics import run_diagnostics
from .infer_contract import infer_contract
from .ingest import ingest_markdown
from .parse_markdown import parse_markdown
from .render_report import write_outputs
from .run_manifest import build_manifest, utc_now


def run_audit(target: str | Path, out_dir: str | Path, command: list[str] | None = None) -> dict[str, object]:
    started_at = utc_now()
    source = ingest_markdown(target)
    parsed = parse_markdown(source)
    contract = infer_contract(parsed)
    diagnostics = run_diagnostics(parsed, contract)

    out_path = Path(out_dir).expanduser().resolve()
    output_paths = {
        "diagnostics_jsonl": out_path / "diagnostics.jsonl",
        "skill_report": out_path / "skill_report.md",
        "remediation_tasks": out_path / "remediation_tasks.md",
        "suggested_patch": out_path / "suggested_patch.md",
        "run_manifest": out_path / "run_manifest.json",
    }
    completed_at = utc_now()
    manifest = build_manifest(
        target=source.path,
        out_dir=out_path,
        command=command or [],
        diagnostics_count=len(diagnostics),
        output_paths=output_paths,
        started_at=started_at,
        completed_at=completed_at,
    )
    write_outputs(out_dir=out_path, target=source.path, diagnostics=diagnostics, manifest=manifest)
    return manifest

