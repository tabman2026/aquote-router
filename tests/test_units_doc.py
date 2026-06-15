from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_units_doc_exists_and_covers_quote_record_and_kline() -> None:
    text = (ROOT / "docs" / "UNITS.md").read_text(encoding="utf-8")

    assert "QuoteRecord" in text
    assert "KlineBar" in text
    for field in ["price", "open", "high", "low", "pre_close", "volume", "amount"]:
        assert f"`{field}`" in text
    for field in ["close", "datetime", "period"]:
        assert f"`{field}`" in text
    assert "pct_chg" in text
    assert "RMB yuan" in text
