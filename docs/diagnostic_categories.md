# Diagnostic Categories

SkillDoctor v0.1 uses these categories:

- `invocation_clarity`: trigger and non-trigger boundaries.
- `input_output_contract`: required inputs and durable outputs.
- `preconditions`: prerequisites before running a workflow.
- `acceptance_criteria`: measurable definition of done.
- `execution_hazards`: commands, writes, destructive actions, and secrets.
- `instruction_conflicts`: contradictory instructions or obligations.
- `security_prompt_injection`: handling of untrusted inspected text.
- `tool_permission_risk`: tool, shell, filesystem, and network boundaries.
- `context_load_discipline`: avoiding unnecessary context expansion.
- `host_adapter_compatibility`: keeping wrappers thin and compatible.
- `verification_gaps`: evidence required before claiming success.
- `maintainer_handoff`: recovery and continuation guidance.

Each diagnostic record includes an ID, category, severity, title, evidence, risk,
recommended fix, patchability, and confidence score.

