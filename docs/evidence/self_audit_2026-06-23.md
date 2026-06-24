# Self-Audit Evidence: 2026-06-23

This file is a manually maintained evidence summary for the historical
SkillDoctor self-audit run completed at `2026-06-23T16:22:18Z`. It summarizes
the generated artifacts without making `runs/**` part of the normal ClaimLint
claim corpus.

## Run Summary

- Command: `skill-doctor audit skills/skill-doctor/SKILL.md --out runs/skill-doctor-self-audit`
- Target: `skills/skill-doctor/SKILL.md`
- Output directory: `runs/skill-doctor-self-audit`
- Validation status: `Passed`
- Diagnostic count: `1`

The run produced all five required SkillDoctor artifacts:

- `diagnostics.jsonl`
- `skill_report.md`
- `remediation_tasks.md`
- `suggested_patch.md`
- `run_manifest.json`

## Diagnostic Summary

The single diagnostic was `SD004`.

- Category: `acceptance_criteria`
- Severity: `major`
- Title: Acceptance criteria are missing
- Evidence: No acceptance criteria or definition-of-done section was inferred.
- Risk: Agents may overstate completion or stop before the skill's required
  outcome is produced.
- Recommended fix: Add measurable acceptance criteria that define the minimum
  complete outcome.

## Evidence Source

This summary is derived from:

- `runs/skill-doctor-self-audit/run_manifest.json`
- `runs/skill-doctor-self-audit/diagnostics.jsonl`

Generated run artifacts remain review evidence, not normative documentation.
