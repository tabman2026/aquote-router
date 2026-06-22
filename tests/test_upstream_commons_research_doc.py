from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UPSTREAM_COMMONS_RESEARCH.md"


def test_upstream_commons_research_doc_exists() -> None:
    assert DOC.exists()


def test_upstream_commons_research_mentions_required_sources() -> None:
    text = DOC.read_text(encoding="utf-8")

    for name in ["AKShare", "efinance", "pytdx", "easyquotation", "baostock", "mootdx"]:
        assert name in text


def test_upstream_commons_research_summarizes_required_commons() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "字段" in text
    assert "单位" in text
    assert "Symbol Format" in text
    assert "K-line Period" in text
    assert "Adjustment" in text
    assert "adapter -> normalize -> validate ->\n   audit -> public record" in text
