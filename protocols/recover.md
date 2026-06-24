# Protocol: Recover

Use this protocol when resuming interrupted SkillDoctor work.

## Steps

1. Read the active working ledger if one was assigned.
2. Inspect `README.md`, `spec/SPEC.md`, `src/skill_doctor/`, and `tests/`.
3. Run the validation protocol if implementation files changed.
4. Mark stale validation as stale before relying on it.

