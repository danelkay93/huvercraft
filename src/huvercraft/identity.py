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
    SELF = auto()
    MARRIED = auto()
    MAIDEN = auto()
    PARTNERSHIP = auto()
    GERMANISED = auto()
    MAGYARISED = auto()


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

_GIVEN_CANONICAL: dict[str, str] = {}
for canonical, variants in GIVEN_NAME_EQUIVALENCES.items():
    for v in variants:
        _GIVEN_CANONICAL_v.lower()] = canonical

SURNAME_EQUIVALENCES: dict[str, frozenset[str]] = {
    "Breuer": frozenset({"Breuer", "Breier", "Brewer"}),
    "Zahler": frozenset({"Zahler", "Záhler"}),
}

_SURNAME_CANONICAL: dict[str, str] = {}
for canonical, variants in SURNAME_EQUIVALENCES.items():
    for v in variants:
        _SURNAME_CANONICAL[v.lower()] = canonical


def strip_diacritics(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_for_search(name: str) -> str:
    stripped = strip_diacritics(name.lower())
    return "".join(c for c in stripped if c.isalnum() or c == " ").strip()


@dataclass(frozen=True)
class MarriedNameParts:
    husband_surname: str
    husband_given: str
    suffix: str
    raw: str

    @property
    def husband_full(self) -> str:
        return f"{self.husband_surname} {self.husband_given}"


def parse_married_name(text: str) -> MarriedNameParts | None:
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


def canonicalize_given(name: str) -> str:
    return _GIVEN_CANONICAL.get(name.lower(), name)


def canonicalize_surname(name: str) -> str:
    return _SURNAME_CANONICAL.get(name.lower(), name)


@dataclass
class IdentityCluster:
    canonical_name: str
    aliases: dict[str, NameRole] = field(default_factory=dict)
    notes: str = ""

    def matches(self, name: str) -> bool:
        norm = normalize_for_search(name)
        return any(normalize_for_search(alias) == norm for alias in self.aliases)


KNOWN_IDENTITIES: list[IdentityCluster] = [
    IdentityCluster(
        canonical_name="Zahler István",
        aliases={
            "Zahler István": NameRole.SELF,
            "Zahler Istvan": NameRole.SELF,
            "Stefan Zahler": NameRole.GERMANISED,
            "Zahler Stefan": NameRole.GERMANISED,
            "Zahler Miksa": NameRole.SELF,
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
        notes="Wife of Zahler István, née Breuer.",
    ),
]


def resolve_identity(name: str) -> IdentityCluster | None:
    for cluster in KNOWN_IDENTITIES:
        if cluster.matches(name):
            return cluster
    return None
