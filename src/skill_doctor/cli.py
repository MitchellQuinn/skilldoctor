from __future__ import annotations

import argparse
import sys

from . import __version__
from .audit import run_audit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skill-doctor",
        description="Audit Markdown agent skills with deterministic diagnostics.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command_name")

    audit_parser = subparsers.add_parser("audit", help="audit one Markdown skill or instruction file")
    audit_parser.add_argument("target", help="Markdown file to audit")
    audit_parser.add_argument("--out", required=True, help="directory for audit output artifacts")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command_name == "audit":
        manifest = run_audit(args.target, args.out, command=["skill-doctor", *(argv or sys.argv[1:])])
        print(f"Wrote SkillDoctor audit to {manifest['output_dir']}")
        print(f"Diagnostics: {manifest['diagnostics_count']}")
        return 0
    build_parser().print_help()
    return 2

