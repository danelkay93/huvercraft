#!/usr/bin/env python3
"""
CLI entry point for huvercraft.

Usage:
    python -m huvercraft /path/to/pdfs
    python -m huvercraft /path/to/pdfs -o results.txt
    python -m huvercraft /path/to/pdfs --json
    echo "some text" | python -m huvercraft --stdin
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from .formatter import to_json, write_report
from .pdf_reader import extract_text, find_pdfs
from .scanner import scan_text

if TYPE_CHECKING:
    from .types import ScanResult


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="huvercraft",
        description="Find Zahler/Breuer printer references in Hungarian texts and PDFs.",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        help="Directory containing PDF files to scan.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Write results to this file (default: stdout).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON.",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read plain text from stdin instead of scanning PDFs.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    results: list[ScanResult] = []

    if args.stdin:
        text = sys.stdin.read()
        results.append(scan_text(text, source="<stdin>"))
    elif args.directory:
        directory = Path(args.directory)
        if not directory.is_dir():
            print(f"Error: {directory} is not a directory", file=sys.stderr)
            return 1

        pdfs = find_pdfs(directory)
        if not pdfs:
            print(f"No PDF files found in {directory}", file=sys.stderr)
            return 1

        print(f"Scanning {len(pdfs)} PDF files...", file=sys.stderr)
        for pdf_path in pdfs:
            print(f"  {pdf_path.name}", file=sys.stderr)
            try:
                text = extract_text(pdf_path)
                results.append(scan_text(text, source=str(pdf_path)))
            except Exception as e:
                print(f"  ⚠ Error: {e}", file=sys.stderr)
    else:
        print("Error: provide a directory or use --stdin", file=sys.stderr)
        return 1

    # Output
    if args.json:
        output_text = to_json(results)
    else:
        from io import StringIO

        buf = StringIO()
        write_report(results, buf)
        output_text = buf.getvalue()

    if args.output:
        args.output.write_text(output_text, encoding="utf-8")
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
