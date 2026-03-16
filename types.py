"""Types and enums for the printer finder pattern library."""

from __future__ import annotations

from enum import StrEnum, auto
from typing import NamedTuple


class MatchCategory(StrEnum):
    """Categories of matches found in text.

    Ordered roughly from most-specific to least-specific.
    The registry iterates in this order, so more-specific
    patterns get first crack at the text.
    """

    # Relational (printer + context)
    PRINTER_WITH_ESTABLISHMENT = auto()
    OWNER_STATEMENT = auto()
    HUNGÁRIA_CONTEXT = auto()
    FOTOMŰVÉSZETI_CONTEXT = auto()
    MARRIED_NAME = auto()
    PARTNERSHIP = auto()

    # Addresses
    LOVAG_ADDRESS = auto()
    NAGYMEZŐ_ADDRESS = auto()
    BUDAPEST_DISTRICT = auto()

    # Standalone
    STANDALONE_ESTABLISHMENT = auto()
    STANDALONE_PRINTER = auto()


class MatchResult(NamedTuple):
    """A single regex match with its location and context."""

    category: MatchCategory
    start: int
    end: int
    text: str
    context: str = ""


class ScanResult(NamedTuple):
    """Results from scanning a single document."""

    source: str
    matches: list[MatchResult]

    @property
    def has_matches(self) -> bool:
        return len(self.matches) > 0

    def by_category(self, *categories: MatchCategory) -> list[MatchResult]:
        """Filter matches by one or more categories."""
        cat_set = set(categories)
        return [m for m in self.matches if m.category in cat_set]

    @property
    def categories_found(self) -> set[MatchCategory]:
        return {m.category for m in self.matches}
