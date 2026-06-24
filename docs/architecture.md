# Architecture

SkillDoctor is a small static-analysis pipeline.

1. Ingest one Markdown file.
2. Parse structural features: frontmatter, headings, bullets, fenced blocks,
   examples, references, and imperative instructions.
3. Infer a conservative skill contract.
4. Run deterministic diagnostic passes against the inferred contract.
5. Assign severity and confidence.
6. Render JSONL and Markdown outputs.
7. Suggest remediation without applying changes.

## Implementation Map

The implementation is intentionally small and local:

- `src/skill_doctor/cli.py` exposes the `skill-doctor audit` command.
- `src/skill_doctor/audit.py` orchestrates the audit pipeline.
- `src/skill_doctor/ingest.py` loads one Markdown target as untrusted text.
- `src/skill_doctor/parse_markdown.py` extracts frontmatter, headings, bullets,
  fenced blocks, and imperative lines.
- `src/skill_doctor/infer_contract.py` infers the conservative skill contract
  used by diagnostics.
- `src/skill_doctor/diagnostics.py` emits deterministic diagnostic records, with
  severity and confidence support from `src/skill_doctor/risk_scoring.py`.
- `src/skill_doctor/render_report.py` writes JSONL and Markdown outputs,
  while `src/skill_doctor/schemas.py` and `src/skill_doctor/run_manifest.py`
  define validation helpers and run metadata.

## Diagnostic Usage And Scope

The Quick Start usage example exercises the diagnostic path with
`skill-doctor audit examples/bad-skill/SKILL.md --out runs/bad-skill`.
`tests/test_cli_audit.py` verifies that this audit writes the required output
artifacts and JSONL diagnostic records.

Boundary evidence:

- Scope: `src/skill_doctor/diagnostics.py` handles diagnostic record creation
  from parsed Markdown and inferred data.
- Scope: `src/skill_doctor/risk_scoring.py` contains severity and confidence
  helper functions.
- Outside this scope: file loading, output writing, run metadata, CLI behavior,
  target mutation, command execution, and external model API calls.

The CLI is the source of execution behavior. The bundled skill wrapper explains
how agents should invoke and interpret the CLI; it must not redefine the CLI
contract.
