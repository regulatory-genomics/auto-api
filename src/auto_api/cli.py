from __future__ import annotations

import argparse
import sys
from pathlib import Path

from auto_api.extractor import extract_api_docs
from auto_api.markdown import render_markdown


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "extract":
        return _run_extract(args)

    parser.print_help()
    return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="auto-api")
    subparsers = parser.add_subparsers(dest="command")

    extract = subparsers.add_parser("extract", help="Extract API docs as Markdown.")
    extract.add_argument("--target", required=True, help="Module/package name or local import path.")
    extract.add_argument(
        "--functions",
        nargs="*",
        help="Optional dotted function/object paths. If omitted, public exposed functions are extracted.",
    )
    extract.add_argument("--output", help="Optional Markdown output path. Prints to stdout if omitted.")
    extract.add_argument("--title", default="API Documentation", help="Markdown document title.")
    extract.add_argument("--fail-on-error", action="store_true", help="Exit non-zero if any API cannot be resolved.")
    return parser


def _run_extract(args: argparse.Namespace) -> int:
    docs = extract_api_docs(args.target, args.functions)
    markdown = render_markdown(docs, title=args.title)

    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)

    if args.fail_on_error and any(doc.error for doc in docs):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
