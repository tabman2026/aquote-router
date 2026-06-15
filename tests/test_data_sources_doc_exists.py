from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_data_sources_doc_exists() -> None:
    assert (ROOT / "docs" / "DATA_SOURCES.md").exists()
