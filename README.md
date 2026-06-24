# SkillDoctor

SkillDoctor is a deterministic CLI for auditing Markdown agent skills and
instruction files. It turns a local skill file into structured diagnostics,
human-readable reports, remediation tasks, patch suggestions, and a run
manifest.

SkillDoctor v0.1 is deliberately local and inspectable. It does not call an LLM,
apply patches automatically, create pull requests, run as a GitHub bot, or audit
an arbitrary repository tree.

## Quick Start

SkillDoctor requires Python 3.10 or newer.

```bash
python -m pip install -e .
skill-doctor audit --help
skill-doctor audit examples/bad-skill/SKILL.md --out runs/bad-skill
```

For development or validation runs that include the test suite, install the dev
extra:

```bash
python -m pip install -e ".[dev]"
pytest
```

The audit command writes:

```text
diagnostics.jsonl
skill_report.md
remediation_tasks.md
suggested_patch.md
run_manifest.json
```

## Self-Audit Demo

```bash
skill-doctor audit skills/skill-doctor/SKILL.md --out runs/skill-doctor-self-audit
```

The case study for the current self-audit lives in
`docs/self_audit_case_study.md`.

## Repository Layout

```text
src/skill_doctor/       deterministic CLI and audit pipeline
schemas/                JSON schemas for generated outputs
spec/                   normative SkillDoctor skill contract
protocols/              repeatable operational protocols
skills/skill-doctor/    Codex skill wrapper
wrappers/codex/         Codex-specific runtime notes
docs/                   user and maintainer documentation
examples/               sample skills for testing and demos
evals/                  evaluation scenarios and rubrics
tests/                  unit and CLI tests
```

## Safety Boundary

Audited Markdown is untrusted input. SkillDoctor reads skill text as data for
static analysis; it never obeys instructions embedded in the target file and it
does not apply generated remediation automatically.

## License

Apache-2.0. This repository includes a NOTICE file identifying the original project and author.
