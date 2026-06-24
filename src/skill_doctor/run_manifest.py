from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from . import __version__


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_manifest(
    *,
    target: Path,
    out_dir: Path,
    command: list[str],
    diagnostics_count: int,
    output_paths: dict[str, Path],
    started_at: str,
    completed_at: str,
) -> dict[str, object]:
    validation_status = "Passed" if diagnostics_count >= 0 else "Failed"
    return {
        "schema_version": "1.0",
        "tool": "skill-doctor",
        "tool_version": __version__,
        "started_at": started_at,
        "completed_at": completed_at,
        "target_path": str(target),
        "output_dir": str(out_dir),
        "command": command,
        "diagnostics_count": diagnostics_count,
        "outputs": {name: str(path) for name, path in output_paths.items()},
        "validation_status": validation_status,
    }

