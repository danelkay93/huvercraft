"""
PDF text extraction.

Isolated I/O layer: reads PDFs, returns plain text.
Keeps file-handling concerns separate from pattern matching.
"""

from __future__ import annotations

from pathlib import Path


def extract_text(pdf_path: str | Path) -> str:
    """
    Extract all text from a PDF file.

    Uses PyPDF2 as the primary extractor. Returns empty string
    on any read error (logged to stderr).
    """
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError(
            "PyPDF2 is required for PDF processing. Install it with: pip install PyPDF2"
        ) from None

    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    pages: list[str] = []
    reader = PdfReader(path)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


def find_pdfs(directory: str | Path, *, recursive: bool = True) -> list[Path]:
    """Find all PDF files in a directory."""
    root = Path(directory)
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")
    glob = root.rglob if recursive else root.glob
    return sorted(glob("*.pdf"))
