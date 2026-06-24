# Protocol: Validate

Use this protocol after implementation changes or before publishing a demo.

## Steps

1. Run `pip install -e .`.
2. Run `skill-doctor audit --help`.
3. Run `skill-doctor audit examples/bad-skill/SKILL.md --out runs/bad-skill`.
4. Validate `diagnostics.jsonl` and `run_manifest.json` against their schemas.
5. Run the test suite.

## Postconditions

Record each check as `Passed`, `Failed`, `Partially Verified`, or `Not Run`.

