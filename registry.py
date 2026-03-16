"""
Compiled pattern registry.

Compiles all composed patterns once at import time, mapping each
to its `MatchCategory`. This is the only place `regex.compile` is called.
"""

import regex

from ..types import MatchCategory
from . import composed as c

# All patterns use these flags
_FLAGS = regex.IGNORECASE | regex.VERBOSE | regex.VERSION1 | regex.UNICODE

# The registry: category → compiled pattern
# Order matters for priority when matches overlap.
PATTERNS: dict[MatchCategory, regex.Pattern[str]] = {
    # Most-specific first
    MatchCategory.PRINTER_WITH_ESTABLISHMENT: regex.compile(c.PRINTER_NEAR_ESTABLISHMENT, _FLAGS),
    MatchCategory.OWNER_STATEMENT: regex.compile(c.OWNER_STATEMENT, _FLAGS),
    MatchCategory.HUNGÁRIA_CONTEXT: regex.compile(c.HUNGÁRIA_CONTEXT, _FLAGS),
    MatchCategory.FOTOMŰVÉSZETI_CONTEXT: regex.compile(c.FOTOMŰVÉSZETI_CONTEXT, _FLAGS),
    MatchCategory.MARRIED_NAME: regex.compile(c.MARRIED_NAME, _FLAGS),
    MatchCategory.PARTNERSHIP: regex.compile(c.PARTNERSHIP, _FLAGS),
    # Addresses
    MatchCategory.LOVAG_ADDRESS: regex.compile(c.LOVAG_ADDRESS, _FLAGS),
    MatchCategory.NAGYMEZŐ_ADDRESS: regex.compile(c.NAGYMEZŐ_ADDRESS, _FLAGS),
    MatchCategory.BUDAPEST_DISTRICT: regex.compile(c.BUDAPEST_DISTRICT_VI, _FLAGS),
    # Standalone / broad
    MatchCategory.STANDALONE_ESTABLISHMENT: regex.compile(c.ANY_ESTABLISHMENT, _FLAGS),
    MatchCategory.STANDALONE_PRINTER: regex.compile(c.PRINTER_NEAR_CITY, _FLAGS),
}
