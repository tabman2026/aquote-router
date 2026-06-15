from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_roadmap_exists_and_has_required_versions() -> None:
    text = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")

    for version in ["v0.2.x", "v0.3.x", "v0.4.x", "v1.0.0"]:
        assert version in text
    assert "error codes" in text
    assert "diagnose" in text
    assert "source policy" in text


def test_roadmap_has_no_trading_decision_content() -> None:
    text = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
    blocked_terms = [
        "Q" + "MT",
        "券" + "商",
        "真实" + "交易",
        "候选" + "股池",
        "买卖" + "点",
        "收益" + "率",
        "胜" + "率",
    ]

    for term in blocked_terms:
        assert term not in text
