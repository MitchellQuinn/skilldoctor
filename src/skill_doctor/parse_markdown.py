from __future__ import annotations

from dataclasses import dataclass
import re

from .ingest import SourceDocument


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FRONTMATTER_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$")
IMPERATIVE_RE = re.compile(
    r"\b(must|must not|should|do not|never|always|run|execute|delete|overwrite|install|apply|create|update|write)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    line: int


@dataclass(frozen=True)
class Bullet:
    text: str
    line: int


@dataclass(frozen=True)
class FencedBlock:
    language: str
    text: str
    start_line: int
    end_line: int


@dataclass(frozen=True)
class MarkdownDocument:
    source: SourceDocument
    frontmatter: dict[str, str]
    body: str
    headings: list[Heading]
    bullets: list[Bullet]
    fenced_blocks: list[FencedBlock]
    imperative_lines: list[Bullet]


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], int]:
    if not lines or lines[0].strip() != "---":
        return {}, 0

    frontmatter: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return frontmatter, index + 1
        match = FRONTMATTER_RE.match(line)
        if match:
            frontmatter[match.group(1).strip()] = match.group(2).strip().strip('"')
    return frontmatter, 0


def parse_markdown(source: SourceDocument) -> MarkdownDocument:
    lines = source.lines
    frontmatter, body_start = parse_frontmatter(lines)
    body_lines = lines[body_start:]
    headings: list[Heading] = []
    bullets: list[Bullet] = []
    fenced_blocks: list[FencedBlock] = []
    imperative_lines: list[Bullet] = []

    in_fence = False
    fence_language = ""
    fence_start = 0
    fence_lines: list[str] = []

    for offset, line in enumerate(body_lines, start=body_start + 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_fence:
                in_fence = True
                fence_language = stripped[3:].strip()
                fence_start = offset
                fence_lines = []
            else:
                fenced_blocks.append(
                    FencedBlock(
                        language=fence_language,
                        text="\n".join(fence_lines),
                        start_line=fence_start,
                        end_line=offset,
                    )
                )
                in_fence = False
                fence_language = ""
                fence_lines = []
            continue

        if in_fence:
            fence_lines.append(line)
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            headings.append(
                Heading(
                    level=len(heading_match.group(1)),
                    title=heading_match.group(2).strip(),
                    line=offset,
                )
            )

        if re.match(r"^\s*[-*+]\s+", line) or re.match(r"^\s*\d+[.)]\s+", line):
            bullets.append(Bullet(text=re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line).strip(), line=offset))

        if IMPERATIVE_RE.search(line):
            imperative_lines.append(Bullet(text=stripped, line=offset))

    if in_fence:
        fenced_blocks.append(
            FencedBlock(
                language=fence_language,
                text="\n".join(fence_lines),
                start_line=fence_start,
                end_line=len(lines),
            )
        )

    return MarkdownDocument(
        source=source,
        frontmatter=frontmatter,
        body="\n".join(body_lines),
        headings=headings,
        bullets=bullets,
        fenced_blocks=fenced_blocks,
        imperative_lines=imperative_lines,
    )


def section_map(document: MarkdownDocument) -> dict[str, str]:
    """Return heading-title keys mapped to the text under each heading."""

    lines = document.source.lines
    sections: dict[str, str] = {}
    for index, heading in enumerate(document.headings):
        next_line = document.headings[index + 1].line if index + 1 < len(document.headings) else len(lines) + 1
        title_key = normalize_title(heading.title)
        content = "\n".join(lines[heading.line: next_line - 1]).strip()
        sections[title_key] = content
    return sections


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")

