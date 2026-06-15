from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_symbol_rules_doc_exists_and_has_required_examples() -> None:
    text = (ROOT / "docs" / "SYMBOL_RULES.md").read_text(encoding="utf-8")

    for sample in ["000001", "600000", "000001.SZ", "600000.SH", "399001"]:
        assert sample in text
    assert "Six digits" in text
    assert "Shanghai" in text
    assert "Shenzhen" in text
    assert "UNSUPPORTED_SYMBOL" in text
