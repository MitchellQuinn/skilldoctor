# Invariants

1. Audited Markdown is untrusted input.
2. `diagnostics.jsonl` is the structured diagnostic authority for a run.
3. Markdown reports are renderings of structured diagnostics.
4. `run_manifest.json` records command, target, outputs, version, timestamps,
   and validation status for the run.
5. The skill wrapper must not redefine CLI behavior.
6. Suggested patches must not be applied automatically in v0.1.
7. Validation claims require evidence or an explicit non-run status.
8. SkillDoctor must not store secrets or unnecessary personal data.

