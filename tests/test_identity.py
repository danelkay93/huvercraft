"""Tests for Layer 2: Identity resolution."""

from __future__ import annotations

import pytest

from huvercraft.identity import (
    canonicalize_given,
    canonicalize_surname,
    normalize_for_search,
    parse_married_name,
    resolve_identity,
    strip_diacritics,
)


class TestMarriedNameParsing:
    def test_standard_né(self) -> None:
        parts = parse_married_name("Zahler Istvánné")
        assert parts is not None
        assert parts.husband_surname == "Zahler"
        assert parts.husband_given == "István"
        assert parts.suffix == "né"

    def test_not_married(self) -> None:
        assert parse_married_name("Breuer Mihály nyomdatulajdonos") is None

    def test_husband_full(self) -> None:
        parts = parse_married_name("Zahler Istvánné")
        assert parts is not None
        assert parts.husband_full == "Zahler István"


class TestCanonicalization:
    @pytest.mark.parametrize(
        ("input_name", "expected"),
        [("Stefan", "István"), ("Max", "Miksa"), ("Lilly", "Lili"), ("Julius", "Gyula"), ("Michael", "Mihály"), ("UnknownName", "UnknownName")],
    )
    def test_given_names(self, input_name: str, expected: str) -> None:
        assert canonicalize_given(input_name) == expected

    @pytest.mark.parametrize(
        ("input_name", "expected"),
        [("Breier", "Breuer"), ("Breuer", "Breuer"), ("SomeOther", "SomeOther")],
    )
    def test_surnames(self, input_name: str, expected: str) -> None:
        assert canonicalize_surname(input_name) == expected


class TestDiacritics:
    def test_strip(self) -> None:
        assert strip_diacritics("Nagymező") == "Nagymezo"

    def test_normalize_for_search(self) -> None:
        assert normalize_for_search("Breuer Mihály") == "breuer mihaly"


class TestIdentityClusters:
    def test_resolve_maiden_name(self) -> None:
        cluster = resolve_identity("Breuer Lili")
        assert cluster is not None
        assert "Zahler Istvánné" in cluster.aliases

    def test_resolve_married_name(self) -> None:
        cluster = resolve_identity("Zahler Istvánné")
        assert cluster is not None
        assert cluster.canonical_name == "Breuer Lili (Zahler Istvánné)"

    def test_unknown_name(self) -> None:
        assert resolve_identity("Kovács Péter") is None
