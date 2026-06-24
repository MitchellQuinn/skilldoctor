# Ownership Model

SkillDoctor owns generated run artifacts under the selected output directory.
It does not own the audited input file and must not mutate it.

Agents using the SkillDoctor wrapper own interpretation and remediation choices
after reviewing the outputs. The CLI owns deterministic generation of
diagnostics and reports.

