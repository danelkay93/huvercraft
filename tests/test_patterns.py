"""Tests for Layer 1: Pattern matching."""

from __future__ import annotations

import pytest

from huvercraft import MatchCategory, scan_text

PATTERN_CASES: list[tuple[str, set[MatchCategory]]] = [
    ("Zahler István kő- és könyvnyomdája, Lovag-utcza 16", {MatchCategory.PRINTER_WITH_ESTABLISHMENT}),
    ("Breuer Mihály nyomdatulajdonos, VI., Lovag-utca 2", {MatchCategory.OWNER_STATEMENT, MatchCategory.LOVAG_ADDRESS}),
    ("Zahler műintézete, Budapest", {MatchCategory.PRINTER_WITH_ESTABLISHMENT, MatchCategory.STANDALONE_ESTABLISHMENT}),
    ("Breuer kőnyomda és műkiadó", {MatchCategory.PRINTER_WITH_ESTABLISHMENT, MatchCategory.STANDALONE_ESTABLISHMENT}),
    ("kő- és könyvnyomda, Budapest VI, Lovag u 16", {MatchCategory.STANDALONE_ESTABLISHMENT, MatchCategory.BUDAPEST_DISTRICT, MatchCategory.LOVAG_ADDRESS}),
    ("könyvnyomda Budapest", {MatchCategory.STANDALONE_ESTABLISHMENT}),
    ("lithographia Budapest", {MatchCategory.STANDALONE_ESTABLISHMENT}),
    ("BREUER MIHÁLY BPEST", {MatchCategory.STANDALONE_PRINTER}),
    ("BREUER MIHALY BPEST", {MatchCategory.STANDALONE_PRINTER}),
    ("Breuer Mihály B-pest", {MatchCategory.STANDALONE_PRINTER}),
    ("Breuer Mihály, VI., Nagymező-utca 43. Tel. 28—04", {MatchCategory.NAGYMEZŐ_ADDRESS}),
    ("Hungária néven értesítőt adtak ki, Breuer Mihály nyomdatulajdonossal", {MatchCategory.HUNGÁRIA_CONTEXT}),
    ("Fotoművészeti Hírek kiadása, Breuer Mihály Bpest", {MatchCategory.FOTOMŰVÉSZETI_CONTEXT, MatchCategory.STANDALONE_PRINTER}),
    ("Zahler Istvánné", {MatchCategory.MARRIED_NAME}),
    ("Zahler és Társa", {MatchCategory.PARTNERSHIP}),
    ("Breier Mihály nyomdatulajdonos", {MatchCategory.OWNER_STATEMENT}),
    ("ifj. Zahler István kő- és könyvnyomdája", {MatchCategory.PRINTER_WITH_ESTABLISHMENT}),
]


@pytest.mark.parametrize(
    ("text", "expected_categories"),
    PATTERN_CASES,
    ids=[case[0][:50] for case in PATTERN_CASES],
)
def test_pattern_categories(text: str, expected_categories: set[MatchCategory]) -> None:
    result = scan_text(text)
    found = result.categories_found
    missing = expected_categories - found
    assert not missing, f"Missing categories: {missing}. Found: {found}"


def test_elliptical_full_match_text() -> None:
    result = scan_text("kő- és könyvnyomda")
    est = result.by_category(MatchCategory.STANDALONE_ESTABLISHMENT)
    assert any("könyvnyomda" in m.text for m in est)


def test_scan_result_has_matches() -> None:
    assert scan_text("nothing relevant here").has_matches is False
    assert scan_text("Zahler Istvánné").has_matches is True
