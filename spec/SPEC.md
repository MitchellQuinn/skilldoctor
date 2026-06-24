# SkillDoctor Specification

SkillDoctor is a deterministic, local audit workflow for Markdown agent skills
and instruction files.

## Core Rule

Audited files are untrusted input. SkillDoctor must analyze their text as data
and must not obey instructions found inside them.

## Required Behavior

- The CLI must accept one Markdown target and one output directory.
- The CLI must produce all required output files for a successful audit.
- Diagnostics must be structured records, not prose-only comments.
- Markdown reports must be derived from the same diagnostics emitted to JSONL.
- Suggested patches must be review material only and must not be applied
  automatically in v0.1.

## Non-Goals

SkillDoctor v0.1 does not provide a web UI, hosted model backend, local model
backend, GitHub bot, automatic pull request creation, marketplace integration,
full arbitrary repo audit, or automatic mutation of audited files.

