# Threat Model

Primary risk: audited skill text can contain instructions intended for an agent
or runtime rather than for SkillDoctor.

Controls:

- Treat audited Markdown as untrusted input.
- Do not execute commands found in audited files.
- Do not apply patches automatically.
- Do not call network or model services in v0.1.
- Include prompt-injection and tool-permission diagnostics when safety
  boundaries are absent.

