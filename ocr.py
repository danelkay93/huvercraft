"""
OCR text normalization for 19th-century Hungarian prints.

Pre-processes text BEFORE regex matching to handle common OCR
misreadings in fraktur/blackletter fonts and historical typesetting.
The original text is preserved alongside the normalized version
so matches can be mapped back to source positions.

This module is intentionally conservative — it only applies
normalizations that are unambiguous in context.
"""

from __future__ import annotations

import re

# -------------------------------------------------------------------------
# Common OCR substitution pairs for Hungarian fraktur
# -------------------------------------------------------------------------
# These are ordered: most-specific first to avoid partial replacements.

_OCR_REPLACEMENTS: list[tuple[str, str]] = [
    # Long-s (ſ) often OCR'd as f
    ("fz", "sz"),  # "fzámára" → "számára"
    ("fs", "ss"),  # doubling error
    # u/n confusion in blackletter
    ("nyonida", "nyomda"),  # n→m in nyomda
    ("nyonidia", "nyomdia"),
    ("nyonmda", "nyomda"),  # transposition
    # Common Hungarian-specific misreads
    ("uteza", "utcza"),  # t→tz confusion
    ("nteza", "ntéze"),  # műintézet misreads
    # ő/ö confusion (OCR often drops the double-dot or umlaut)
    # These are handled more carefully — only in known contexts
]

# Whitespace normalization: historical OCR often inserts spaces mid-word
# e.g., "k ő n y v" → "könyv"
# This is dangerous to do globally, so we only do it for known terms.
_SPACED_TERMS: list[tuple[str, str]] = [
    (r"n\s*y\s*o\s*m\s*d\s*[aá]", "nyomda"),
    (r"k\s*ö\s*n\s*y\s*v", "könyv"),
    (r"m\s*ű\s*i\s*n\s*t\s*é\s*z\s*e\s*t", "műintézet"),
]


def normalize_ocr(text: str) -> str:
    """
    Apply conservative OCR corrections to `text`.

    Returns the normalized text. Call this before passing
    text to `scan_text()` for better recall on messy OCR.
    """
    result = text

    # Simple replacements (case-insensitive)
    for bad, good in _OCR_REPLACEMENTS:
        # Use re for case-insensitive replace while preserving surrounding case
        result = re.sub(re.escape(bad), good, result, flags=re.IGNORECASE)

    # Spaced-out term repairs
    for spaced_pattern, replacement in _SPACED_TERMS:
        result = re.sub(spaced_pattern, replacement, result, flags=re.IGNORECASE)

    return result


def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces/tabs into single spaces, strip lines."""
    return re.sub(r"[ \t]+", " ", text).strip()
