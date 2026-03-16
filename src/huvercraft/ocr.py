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

_OCR_REPLACEMENTS: list[tuple[str, str]] = [
    ("fz", "sz"),
    ("fs", "ss"),
    ("nyonida", "nyomda"),
    ("nyonidia", "nyomdia"),
    ("nyonmda", "nyomda"),
    ("uteza", "utcza"),
    ("nteza", "ntéze"),
]

_SPACED_TERMS: list[tuple[str, str]] = [
    (r"n\s*y\s*o\s*m\s*d\s*[aá]", "nyomda"),
    (r"k\s*ö\s*n\s*y\s*v", "könyv"),
    (r"m\s*ű\s*i\s*n\s*t\s*é\s*z\s*e\s*t", "műintézet"),
]


def normalize_ocr(text: str) -> str:
    result = text
    for bad, good in _OCR_REPLACEMENTS:
        result = re.sub(re.escape(bad), good, result, flags=re.IGNORECASE)
    for spaced_pattern, replacement in _SPACED_TERMS:
        result = re.sub(spaced_pattern, replacement, result, flags=re.IGNORECASE)
    return result


def normalize_whitespace(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text).strip()
