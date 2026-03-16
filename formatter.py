"""
Output formatting for scan results.

Separated from scanning so results can be formatted for
terminal, file, JSON, or any future output target.
"""

from __future__ import annotations

import json
from typing import TextIO

from .types import MatchCategory, ScanResult


def format_terminal(result: ScanResult) -> str:
    """Human-readable format for terminal output."""
    if not result.has_matches:
        return ""

    lines = [
        f"\n{'=' * 72}",
        f"  {result.source}",
        f"{'=' * 72}",
    ]

    # Group by category for readability
    for category in MatchCategory:
        hits = result.by_category(category)
        if not hits:
            continue
        lines.append(f"\n  [{category.value}]")
        for hit in hits:
            lines.append(f"    pos {hit.start:>5}: {hit.text}")
            lines.append(f"             {hit.context}")

    return "\n".join(lines)


def write_report(
    results: list[ScanResult],
    output: TextIO,
) -> None:
    """Write a batch report to a text stream."""
    matched = [r for r in results if r.has_matches]
    total_hits = sum(len(r.matches) for r in matched)

    output.write(f"Scanned {len(results)} files, {len(matched)} with matches ")
    output.write(f"({total_hits} total hits)\n")

    for result in matched:
        output.write(format_terminal(result))
        output.write("\n")


def to_json(results: list[ScanResult]) -> str:
    """Serialize results to JSON for programmatic consumption."""
    return json.dumps(
        [
            {
                "source": r.source,
                "matches": [
                    {
                        "category": m.category.value,
                        "start": m.start,
                        "end": m.end,
                        "text": m.text,
                    }
                    for m in r.matches
                ],
            }
            for r in results
            if r.has_matches
        ],
        indent=2,
        ensure_ascii=False,
    )
