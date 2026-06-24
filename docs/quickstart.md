# Quickstart

SkillDoctor requires Python 3.10 or newer.

```bash
python -m pip install -e .
skill-doctor audit examples/bad-skill/SKILL.md --out runs/bad-skill
```

Open `runs/bad-skill/skill_report.md` for the human-readable report and
`runs/bad-skill/diagnostics.jsonl` for structured records.
