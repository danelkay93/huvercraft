"""
Text scanner for printer references.

Pure logic: takes text in, returns structured results out.
No file I/O, no printing, no side effects.
"""

from __future__ import annotations

from .patterns.registry import PATTERNS
from .types import MatchResult, ScanResult

# How many characters of surrounding context to capture
_CONTEXT_RADIUS = 60


def scan_text(text: str, *, source: str = "<string>") -> ScanResult:
    """
    Scan `text` for all Zahler/Breuer printer references.

    Returns a `ScanResult` with every match tagged by category,
    including a snippet of surrounding context for each hit.
    """
    matches: list[MatchResult] = []

    for category, pattern in PATTERNS.items():
        for m in pattern.finditer(text):
            ctx_start = max(0, m.start() - _CONTEXT_RADIUS)
            ctx_end = min(len(text), m.end() + _CONTEXT_RADIUS)
            context = text[ctx_start:ctx_end].replace("\n", " ")

            matches.append(
                MatchResult(
                    category=category,
                    start=m.start(),
                    end=m.end(),
                    text=m.group().strip(),
                    context=f"...{context}...",
                )
            )

    # Sort by position in document
    matches.sort(key=lambda r: r.start)
    return ScanResult(source=source, matches=matches)
