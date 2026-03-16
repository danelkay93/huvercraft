"""Tests for Layer 1: Pattern matching."""

from __future__ import annotations

import pytest

from huvercraft import MatchCategory, scan_text

# (input_text, set_of_expected_categories)
PATTERN_CASES: list[tuple[str, set[MatchCategory]]] = [
    # ── Core printer + establishment ──────────────────────────────────
    (
        "Zahler István kő- és könyvnyomdája, Lovag-utcza 16",
        {MatchCategory.PRINTER_WITH_ESTABLISHMENT},
    ),
    (
        "Breuer Mihály nyomdatulajdonos, VI., Lovag-utca 2",
        {MatchCategory.OWNER_STATEMENT, MatchCategory.LOVAG_ADDRESS},
    ),
    (
        "Zahler műintézete, Budapest",
        {MatchCategory.PRINTER_WITH_ESTABLISHMENT, MatchCategory.STANDALONE_ESTABLISHMENT},
    ),
    (
        "Breuer kőnyomda és műkiadó",
        {MatchCategory.PRINTER_WITH_ESTABLISHMENT, MatchCategory.STANDALONE_ESTABLISHMENT},
    ),
    # ── Elliptical / compound nyomda ──────────────────────────────────
    (
        "kő- és könyvnyomda, Budapest VI, Lovag u 16",
        {
            MatchCategory.STANDALONE_ESTABLISHMENT,
            MatchCategory.BUDAPEST_DISTRICT,
            MatchCategory.LOVAG_ADDRESS,
        },
    ),
    (
        "könyvnyomda Budapest",
        {MatchCategory.STANDALONE_ESTABLISHMENT},
    ),
    (
        "lithographia Budapest",
        {MatchCategory.STANDALONE_ESTABLISHMENT},
    ),
    # ── City abbreviations ────────────────────────────────────────────
    (
        "BREUER MIHÁLY BPEST",
        {MatchCategory.STANDALONE_PRINTER},
    ),
    (
        "BREUER MIHALY BPEST",
        {MatchCategory.STANDALONE_PRINTER},
    ),
    (
        "Breuer Mihály B-pest",
        {MatchCategory.STANDALONE_PRINTER},
    ),
    # ── Addresses ─────────────────────────────────────────────────────
    (
        "Breuer Mihály, VI., Nagymező-utca 43. Tel. 28—04",
        {MatchCategory.NAGYMEZŐ_ADDRESS},
    ),
    # ── Contextual ────────────────────────────────────────────────────
    (
        "Hungária néven értesítőt adtak ki, Breuer Mihály nyomdatulajdonossal",
        {MatchCategory.HUNGÁRIA_CONTEXT},
    ),
    (
        "Fotoművészeti Hírek kiadása, Breuer Mihály Bpest",
        {MatchCategory.FOTOMŰVÉSZETI_CONTEXT, MatchCategory.STANDALONE_PRINTER},
    ),
    # ── Married name ──────────────────────────────────────────────────
    (
        "Zahler Istvánné",
        {MatchCategory.MARRIED_NAME},
    ),
    # ── Partnership ───────────────────────────────────────────────────
    (
        "Zahler és Társa",
        {MatchCategory.PARTNERSHIP},
    ),
    # ── Orthographic variants ─────────────────────────────────────────
    (
        "Breier Mihály nyomdatulajdonos",
        {MatchCategory.OWNER_STATEMENT},
    ),
    # ── Titles ────────────────────────────────────────────────────────
    (
        "ifj. Zahler István kő- és könyvnyomdája",
        {MatchCategory.PRINTER_WITH_ESTABLISHMENT},
    ),
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
    """Regression: elliptical 'kő- és könyvnyomda' must not truncate."""
    result = scan_text("kő- és könyvnyomda")
    establishment_matches = result.by_category(MatchCategory.STANDALONE_ESTABLISHMENT)
    assert any("könyvnyomda" in m.text for m in establishment_matches)


def test_scan_result_has_matches() -> None:
    assert scan_text("nothing relevant here").has_matches is False
    assert scan_text("Zahler Istvánné").has_matches is True
