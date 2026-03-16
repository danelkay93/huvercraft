"""
Identity resolution for Hungarian historical names.

This module handles the messy reality that one person may appear under
many different names across records:

  - Married-name suffix (-né): Zahler Istvánné → wife of István Zahler
  - Cross-border equivalences: István ↔ Stefan, Miksa ↔ Max
  - Orthographic variants: Breuer ↔ Breier, utca ↔ utcza
  - Magyarization: Germanic surnames replaced with Hungarian ones
  - OCR errors: common misreadings in blackletter/fraktur

The approach is a lightweight "identity cluster" — a set of known
aliases for the same person. This is NOT a general NER system; it's
a curated lookup for the specific printer network under study.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field
from enum import StrEnum, auto


class NameRole(StrEnum):
    """How a name relates to the person it refers to."""

    SELF = auto()  # direct reference
    MARRIED = auto()  # -né form (refers to spouse's name)
    MAIDEN = auto()  # birth surname used after marriage
    PARTNERSHIP = auto()  # business entity name
    GERMANISED = auto()  # cross-border spelling
    MAGYARISED = auto()  # hungarianised form


# -------------------------------------------------------------------------
# Cross-border first-name equivalences
# -------------------------------------------------------------------------

GIVEN_NAME_EQUIVALENCES: dict[str, frozenset[str]] = {
    "István": frozenset({"István", "Stefan", "Stephan", "Stefán"}),
    "Mihály": frozenset({"Mihály", "Michael", "Mihael"}),
    "Gyula": frozenset({"Gyula", "Julius"}),
    "Miksa": frozenset({"Miksa", "Max", "Maximilian"}),
    "Lili": frozenset({"Lili", "Lilly", "Lily", "Lille", "Lilli"}),
    "János": frozenset({"János", "Johann", "Johan", "John"}),
    "József": frozenset({"József", "Joseph", "Josef"}),
    "Sándor": frozenset({"Sándor", "Alexander"}),
    "Károly": frozenset({"Károly", "Karl", "Carl", "Charles"}),
    "Ferenc": frozenset({"Ferenc", "Franz", "Francis"}),
}

# Build reverse lookup: any variant → canonical (first key)
_GIVEN_CANONICAL: dict[str, str] = {}
for canonical, variants in GIVEN_NAME_EQUIVALENCES.items():
    for v in variants:
        _GIVEN_CANONICAL[v.lower()] = canonical


# -------------------------------------------------------------------------
# Surname orthographic variants (OCR + historical)
# -------------------------------------------------------------------------

SURNAME_EQUIVALENCES: dict[str, frozenset[str]] = {
    "Breuer": frozenset({"Breuer", "Breier", "Brewer"}),
    "Zahler": frozenset({"Zahler", "Záhler"}),
}

_SURNAME_CANONICAL: dict[str, str] = {}
for canonical, variants in SURNAME_EQUIVALENCES.items():
    for v in variants:
        _SURNAME_CANONICAL[v.lower()] = canonical


# -------------------------------------------------------------------------
# Diacritical normalization
# -------------------------------------------------------------------------


def strip_diacritics(text: str) -> str:
    """
    Remove diacritical marks for indexing purposes.

    Preserves the base letter: ő→o, á→a, é→e, etc.
    The original text should be kept for display; this is
    only for search/comparison.
    """
    # Decompose then strip combining marks
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_for_search(name: str) -> str:
    """Normalize a name for fuzzy comparison: lowercase, no diacritics, no punctuation."""
    stripped = strip_diacritics(name.lower())
    return "".join(c for c in stripped if c.isalnum() or c == " ").strip()


# -------------------------------------------------------------------------
# -né suffix handling
# -------------------------------------------------------------------------


@dataclass(frozen=True)
class MarriedNameParts:
    """Result of parsing a Hungarian married name."""

    husband_surname: str
    husband_given: str
    suffix: str  # "né", "neé", etc.
    raw: str

    @property
    def husband_full(self) -> str:
        return f"{self.husband_surname} {self.husband_given}"


def parse_married_name(text: str) -> MarriedNameParts | None:
    """
    Parse a -né married-name form.

    "Zahler Istvánné" → MarriedNameParts(husband_surname="Zahler",
                                          husband_given="István", ...)
    Returns None if the text doesn't contain a -né form.
    """
    import regex

    pattern = regex.compile(
        r"\b(?P<surname>\p{Lu}\p{Ll}+)\s+"
        r"(?P<given>\p{Lu}\p{Ll}+)"
        r"(?P<suffix>n[eé](?:nek)?)\b",
        regex.VERSION1 | regex.UNICODE,
    )
    m = pattern.search(text)
    if not m:
        return None
    return MarriedNameParts(
        husband_surname=m.group("surname"),
        husband_given=m.group("given"),
        suffix=m.group("suffix"),
        raw=m.group(0),
    )


# -------------------------------------------------------------------------
# Canonicalization
# -------------------------------------------------------------------------


def canonicalize_given(name: str) -> str:
    """Map a given name to its canonical Hungarian form, or return as-is."""
    return _GIVEN_CANONICAL.get(name.lower(), name)


def canonicalize_surname(name: str) -> str:
    """Map a surname to its canonical form, or return as-is."""
    return _SURNAME_CANONICAL.get(name.lower(), name)


# -------------------------------------------------------------------------
# Identity clusters (curated for this printer network)
# -------------------------------------------------------------------------


@dataclass
class IdentityCluster:
    """
    A set of name-forms that all refer to the same real person.

    This is a curated lookup, not a probabilistic model.
    Each alias carries a `NameRole` explaining the relationship.
    """

    canonical_name: str
    aliases: dict[str, NameRole] = field(default_factory=dict)
    notes: str = ""

    def matches(self, name: str) -> bool:
        """Check if a name (case-insensitive) belongs to this cluster."""
        norm = normalize_for_search(name)
        return any(normalize_for_search(alias) == norm for alias in self.aliases)


# Pre-built clusters for the Zahler/Breuer network
KNOWN_IDENTITIES: list[IdentityCluster] = [
    IdentityCluster(
        canonical_name="Zahler István",
        aliases={
            "Zahler István": NameRole.SELF,
            "Zahler Istvan": NameRole.SELF,
            "Stefan Zahler": NameRole.GERMANISED,
            "Zahler Stefan": NameRole.GERMANISED,
            "Zahler Miksa": NameRole.SELF,  # same person? or relative — needs research
        },
        notes="Printer, kő- és könyvnyomda, Lovag utca 16",
    ),
    IdentityCluster(
        canonical_name="Breuer Mihály",
        aliases={
            "Breuer Mihály": NameRole.SELF,
            "Breuer Mihaly": NameRole.SELF,
            "Breier Mihály": NameRole.SELF,
            "Michael Breuer": NameRole.GERMANISED,
            "Breuer Mihály nyomdatulajdonos": NameRole.SELF,
        },
        notes="Nyomdatulajdonos, VI. Nagymező utca 43 / Lovag utca 2",
    ),
    IdentityCluster(
        canonical_name="Breuer Lili (Zahler Istvánné)",
        aliases={
            "Breuer Lili": NameRole.MAIDEN,
            "Breuer Lilly": NameRole.MAIDEN,
            "Breuer Lily": NameRole.MAIDEN,
            "Zahler Istvánné": NameRole.MARRIED,
            "Zahler Istvanné": NameRole.MARRIED,
            "Zahler Istvánnénak": NameRole.MARRIED,
            "Lili Zahler": NameRole.GERMANISED,
            "Lilly Zahler": NameRole.GERMANISED,
        },
        notes="Wife of Zahler István, née Breuer. Used maiden name for asset purchases.",
    ),
]


def resolve_identity(name: str) -> IdentityCluster | None:
    """Look up which identity cluster a name belongs to, if any."""
    for cluster in KNOWN_IDENTITIES:
        if cluster.matches(name):
            return cluster
    return None
