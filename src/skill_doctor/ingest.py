from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceDocument:
    """A Markdown file loaded as untrusted audit input."""

    path: Path
    text: str

    @property
    def lines(self) -> list[str]:
        return self.text.splitlines()


def ingest_markdown(target: str | Path) -> SourceDocument:
    """Read one Markdown target from disk.

    The returned text is data for analysis only. Callers must not execute or
    obey instructions found inside it.
    """

    path = Path(target).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"target does not exist: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"target is not a file: {path}")
    if path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError(f"target must be a Markdown file: {path}")
    return SourceDocument(path=path, text=path.read_text(encoding="utf-8"))

