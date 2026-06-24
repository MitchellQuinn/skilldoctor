I read the SkillDoctor concept and ideation notes in [SkillDoctor Concept Capture v0.1.md](<D:/Transfer/Starcroft/Documents/Obsidian Vaults/Project Moomin/Project Ideas/Skill Doctor/SkillDoctor Concept Capture v0.1.md>) and [Conversation - Skill Doctor Ideation.md](<D:/Transfer/Starcroft/Documents/Obsidian Vaults/Project Moomin/Project Ideas/Skill Doctor/Conversation - Skill Doctor Ideation.md>).

My recommendation: build v0.1 as a **small deterministic CLI with a Codex skill wrapper**, not as a broad LLM platform. The core signal is: `skill/instruction file -> structured diagnostics -> remediation report -> optional patch`.

**SkillDoctor V0.1 Plan**
**Product Shape**
Build `skill-doctor` as a Python CLI that audits local Markdown instruction files:

```bash
skill-doctor audit \
  --target skills/skill-doctor/SKILL.md \
  --out runs/skill-doctor-self-audit
```

Required outputs:

```text
diagnostics.jsonl
skill_report.md
remediation_tasks.md
suggested_patch.md
run_manifest.json
```

The first public demo should be:

```text
SkillDoctor audits SkillDoctor.
SkillDoctor finds issues.
SkillDoctor fixes its own first draft.
```

**Repository Structure**
```text
skill-doctor/
  README.md
  pyproject.toml
  AGENTS.md

  workflows/
    skill_audit.yml

  schemas/
    diagnostic_record.schema.json
    run_manifest.schema.json

  docs/
    architecture.md
    diagnostic_categories.md
    runtime_contract.md
    self_audit_case_study.md

  skills/
    skill-doctor/
      SKILL.md
      references/
        diagnostic_categories.md
        output_contract.md

  examples/
    bad-skill/
      SKILL.md
    good-skill/
      SKILL.md

  src/
    skill_doctor/
      cli.py
      ingest.py
      parse_markdown.py
      infer_contract.py
      diagnostics.py
      risk_scoring.py
      render_report.py
      schemas.py
      run_manifest.py

  tests/
    fixtures/
    test_cli_audit.py
    test_diagnostics.py
    test_schema_validation.py
```

**Diagnostic Record**
Each finding should be structured, not just prose:

```json
{
  "diagnostic_id": "SD001",
  "category": "invocation_clarity",
  "severity": "major",
  "title": "Trigger description is too broad",
  "evidence": "The skill says to use it for 'agent workflows' without defining non-use cases.",
  "risk": "Agent may over-apply the skill to unrelated prompt or repo-review tasks.",
  "recommended_fix": "Add a 'Use when' and 'Do not use when' section.",
  "patchable": true
}
```

Core categories:

```text
invocation_clarity
input_output_contract
preconditions
acceptance_criteria
execution_hazards
instruction_conflicts
security_prompt_injection
tool_permission_risk
context_load_discipline
host_adapter_compatibility
verification_gaps
maintainer_handoff
```

**Pipeline**
1. Ingest one target Markdown file or a small manifest-selected set of files.
2. Parse frontmatter, headings, bullets, fenced commands, examples, references, and imperative instructions.
3. Infer the skill contract:
   `purpose`, `use_when`, `do_not_use_when`, `inputs`, `outputs`, `tools`, `preconditions`, `failure_behavior`, `acceptance_criteria`.
4. Run deterministic diagnostic passes against that inferred contract.
5. Score risks by severity and confidence.
6. Render Markdown and JSONL outputs.
7. Generate conservative patch suggestions, but do not auto-apply them in v0.1.

**Important V0.1 Design Choice**
Do not require an LLM API. The first version can be heuristic and still useful. Codex can later use the report and optional skill wrapper to add deeper judgement, but the tool itself should run locally and reproducibly.

**Implementation Order**
1. Create skeleton, package config, CLI stub, and fixed output contract.
2. Add JSON schemas for diagnostics and run manifests.
3. Implement Markdown ingestion and simple structural parsing.
4. Implement contract inference with conservative heuristics.
5. Implement diagnostic passes for the highest-value failures:
   invocation ambiguity, missing outputs, missing acceptance criteria, unsafe overbreadth, missing non-goals, prompt-injection exposure, missing smoke test.
6. Add report rendering.
7. Add `examples/bad-skill/SKILL.md` and expected report.
8. Write `skills/skill-doctor/SKILL.md`.
9. Run SkillDoctor against its own skill.
10. Use that output to write `docs/self_audit_case_study.md`.

**Acceptance Criteria**
V0.1 is complete when:

```text
pip install -e . works
skill-doctor audit --help works
skill-doctor audit examples/bad-skill/SKILL.md --out runs/bad-skill works
all five required output files are created
diagnostics.jsonl validates against schema
the tool never treats audited skill text as instructions to obey
the self-audit produces at least one real finding
README shows the self-audit demo clearly
tests pass
```

**Non-Goals For V0.1**
Do not build:

```text
web UI
GitHub bot
automatic PR creation
hosted model backend
local model backend
full arbitrary repo audit
plugin marketplace integration
complex multi-agent orchestration
automatic mutation of audited files
```

The key implementation principle is the same as ClaimLint: make the workflow inspectable. SkillDoctor should not be “an agent comments on a skill.” It should be a small static-analysis pipeline with explicit contracts, structured diagnostics, bounded claims, and remediation outputs.