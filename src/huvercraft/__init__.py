"""
huvercraft — Search historical Hungarian texts for Zahler/Breuer printer references.

Three layers:
  1. Pattern matching (patterns/) — regex-based text scanning
  2. OCR normalization (ocr) — pre-processing for messy fraktur OCR
  3. Identity resolution (identity) — alias clusters, -né parsing, cross-border names

Uses the `regex` package (V1 behavior) for full Unicode property support.
"""

from .identity import (
    canonicalize_given,
    canonicalize_surname,
    normalize_for_search,
    parse_married_name,
    resolve_identity,
    strip_diacritics,
)
from .ocr import normalize_ocr
from .scanner import scan_text
from .types import MatchCategory, MatchResult, ScanResult

__all__ = [
    "MatchCategory",
    "MatchResult",
    "ScanResult",
    "canonicalize_given",
    "canonicalize_surname",
    "normalize_for_search",
    "normalize_ocr",
    "parse_married_name",
    "resolve_identity",
    "scan_text",
    "strip_diacritics",
]
