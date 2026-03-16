# Copilot Instructions for huvercraft

A Python regex toolkit for finding historical Hungarian printer attributions
(Zahler/Breuer network, Budapest, ~1890–1940) in OCR'd texts.

## Architecture

- **Atoms → Composed → Registry → Scanner.**
- Never compile regex outside `registry.py`.
- Every spelling variant defined ONCE in `atoms.py`.
- Types are `StrEnum`s and `NamedTuple`s.

## Code Style

- Python >=3.13, `from __future__ import annotations`.
- `regex` package with `VERSION1` — not stdlib `re`.
- Ruff for linting and formatting.
- `RUF001`/`RUF002`/`RUF003` disabled (Hungarian Unicode).
