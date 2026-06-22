from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_RULES = ROOT / "docs" / "ADAPTER_UNIT_RULES_DRAFT_V040.md"


def test_adapter_candidate_unit_rules_cover_sources_and_standard_units() -> None:
    text = UNIT_RULES.read_text(encoding="utf-8")
    for source in ["efinance", "baostock", "mootdx"]:
        assert source in text
    assert "volume_shares" in text
    assert "amount_yuan" in text


def test_adapter_candidate_unit_rules_mark_uncertain_units_unknown() -> None:
    text = UNIT_RULES.read_text(encoding="utf-8")
    assert "unknown" in text
    assert "| efinance realtime | `成交量` | unknown |" in text
    assert "| baostock K-line | `volume` | unknown |" in text
    assert "| mootdx quote | `vol` | unknown |" in text
