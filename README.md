# huvercraft

Regex toolkit for finding historical Hungarian printer attributions in OCR'd
texts and PDFs. Targets the Zahler/Breuer printing network (Budapest,
~1890–1940).

## What it does

Scans text for references to printing houses, printer names, addresses, and
related context — accounting for the full mess of historical Hungarian
orthography:

- **Compound & elliptical forms:** `könyvnyomda`, `kő- és könyvnyomda`
- **Establishment terms:** `nyomda`, `műintézet`, `műkiadó`, `lithographia`
- **Historical spelling:** `utca`/`utcza`, `ő`/`o`, `á`/`a`
- **City abbreviations:** `Budapest`, `Bpest`, `Bp.`, `BPEST`, `B-pest`
- **Married names:** `Zahler Istvánné` (the `-né` suffix)
- **Partnership forms:** `és Társa`, `Testvérek`, `Rt.`
- **Cross-border names:** `István`↔`Stefan`, `Miksa`↔`Max`, `Breuer`↔`Breier`
- **OCR normalization:** fraktur misreads, spaced-out words

## Install

```bash
uv add huvercraft
# or
pip install huvercraft
```

For PDF scanning:
```bash
uv add "huvercraft[pdf]"
```

## Quick start

```python
from huvercraft import scan_text

result = scan_text("Zahler István kő- és könyvnyomdája, Lovag-utcza 16")
for match in result.matches:
    print(f"[{match.category}] {match.text}")
```

## CLI

```bash
# Scan a directory of PDFs
huvercraft /path/to/auction_catalogues -o results.txt

# Read from stdin
echo "Breuer Mihály nyomdatulajdonos" | huvercraft --stdin

# JSON output
huvercraft /path/to/pdfs --json
```

## Identity resolution

```python
from huvercraft import parse_married_name, resolve_identity, canonicalize_given

# Parse married names
parts = parse_married_name("Zahler Istvánné")
# → MarriedNameParts(husband_surname="Zahler", husband_given="István", ...)

# Cross-reference aliases
cluster = resolve_identity("Breuer Lili")
# → IdentityCluster with aliases including "Zahler Istvánné"

# Normalize cross-border given names
canonicalize_given("Stefan")  # → "István"
canonicalize_given("Max")     # → "Miksa"
```

## Architecture

```
src/huvercraft/
├── patterns/
│   ├── atoms.py       ← atomic regex fragments (DRY building blocks)
│   ├── composed.py    ← patterns built from atoms
│   └── registry.py    ← compiled patterns mapped to categories
├── scanner.py         ← pure matching logic (text in → results out)
├── identity.py        ← name normalization, -né parsing, alias clusters
├── ocr.py             ← OCR pre-processing for fraktur misreads
├── pdf_reader.py      ← PDF text extraction (I/O layer)
├── formatter.py       ← output formatting (terminal, file, JSON)
├── types.py           ← StrEnums and NamedTuples
└── __main__.py        ← CLI entry point
```

## Development

```bash
uv sync --all-extras
uv run ruff check src/ tests/
uv run pytest
```

## License

MIT
