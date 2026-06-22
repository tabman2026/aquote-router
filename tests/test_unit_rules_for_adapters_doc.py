from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UNIT_RULES_FOR_ADAPTERS.md"


def test_unit_rules_for_adapters_doc_exists() -> None:
    assert DOC.exists()


def test_unit_rules_for_adapters_contains_required_rules() -> None:
    text = DOC.read_text(encoding="utf-8")

    for marker in ["volume_shares", "amount_yuan", "手转股", "万元转元"]:
        assert marker in text
