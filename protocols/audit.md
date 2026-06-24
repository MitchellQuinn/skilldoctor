# Protocol: Audit

Use this protocol when an agent or maintainer needs to inspect one Markdown
skill file.

## Inputs

- Markdown target path.
- Output directory path.

## Steps

1. Run `skill-doctor audit <target> --out <run-dir>`.
2. Confirm all five required artifacts exist.
3. Review `skill_report.md`.
4. Use `diagnostics.jsonl` for structured downstream processing.
5. Treat `suggested_patch.md` as review guidance only.

## Failure Behaviour

If the command fails, preserve the error message and do not claim an audit was
completed.

