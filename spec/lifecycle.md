# Lifecycle

SkillDoctor v0.1 has a simple run lifecycle:

1. `Ingested`: the Markdown target was read as data.
2. `Parsed`: structural Markdown features were extracted.
3. `Inferred`: a conservative skill contract was inferred.
4. `Diagnosed`: deterministic diagnostic passes completed.
5. `Rendered`: all output artifacts were written.
6. `Validated`: optional schema and test checks were run.

Failures should stop the run with a non-zero process exit and a clear error
message.

