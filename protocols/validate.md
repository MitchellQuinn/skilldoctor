# Protocol: Validate

Use this protocol after implementation changes or before publishing a demo.

## Steps

1. Confirm Python 3.10 or newer is active.
2. Run `python -m pip install -e ".[dev]"` for a full validation environment.
   Use `python -m pip install -e .` only when validating the CLI without tests.
3. Run `skill-doctor audit --help`.
4. Run `skill-doctor audit examples/bad-skill/SKILL.md --out runs/bad-skill`.
5. Validate `diagnostics.jsonl` and `run_manifest.json` against their schemas.
6. Run `pytest`.

## Postconditions

Record each check as `Passed`, `Failed`, `Partially Verified`, or `Not Run`.
