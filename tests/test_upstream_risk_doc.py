from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_upstream_risk_doc_exists_and_contains_required_boundaries() -> None:
    text = (ROOT / "docs" / "UPSTREAM_LICENSE_AND_RISK.md").read_text(encoding="utf-8")

    assert "does not produce market data" in text
    assert "does not claim official exchange-authorized data" in text
    assert "pytdx" in text
    assert "easyquotation" in text
    assert "license" in text.lower()
    assert "delayed, unavailable, incomplete" in text
    assert "K-line APIs are pytdx-only" in text
