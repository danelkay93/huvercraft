"""Tests for Layer 3: OCR normalization."""

from __future__ import annotations

import pytest

from huvercraft.ocr import normalize_ocr, normalize_whitespace


@pytest.mark.parametrize(
    ("raw", "expected_substring"),
    [
        ("nyonida", "nyomda"),
        ("nyonmda", "nyomda"),
        ("n y o m d a", "nyomda"),
        ("m ű i n t é z e t", "műintézet"),
    ],
)
def test_ocr_repairs(raw: str, expected_substring: str) -> None:
    result = normalize_ocr(raw)
    assert expected_substring in result.lower()


def test_whitespace_normalization() -> None:
    assert normalize_whitespace("  hello   world  ") == "hello world"
