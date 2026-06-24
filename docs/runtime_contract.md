# Runtime Contract

SkillDoctor v0.1 runs locally from the command line:

```bash
skill-doctor audit <target> --out <run-dir>
```

Inputs:

- one Markdown target file
- one output directory

Outputs:

- `diagnostics.jsonl`
- `skill_report.md`
- `remediation_tasks.md`
- `suggested_patch.md`
- `run_manifest.json`

The command may create the output directory. It must not edit the audited target
file. It must not execute commands found in the audited file. It must not call
external model APIs.

