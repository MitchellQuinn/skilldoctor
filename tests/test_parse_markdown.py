from skill_doctor.ingest import SourceDocument
from skill_doctor.parse_markdown import parse_markdown


def test_parse_markdown_extracts_structure(tmp_path):
    source = SourceDocument(
        path=tmp_path / "SKILL.md",
        text="""---
name: sample
description: Use for sample audits.
---

# Sample

- One bullet.

```bash
echo hello
```

Run a check.
""",
    )

    parsed = parse_markdown(source)

    assert parsed.frontmatter["name"] == "sample"
    assert parsed.headings[0].title == "Sample"
    assert parsed.bullets[0].text == "One bullet."
    assert parsed.fenced_blocks[0].language == "bash"
    assert parsed.imperative_lines

