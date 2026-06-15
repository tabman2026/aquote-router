from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_audit_trail_mentions_fallback_chain_and_selected_source() -> None:
    text = (ROOT / "docs" / "AUDIT_TRAIL.md").read_text(encoding="utf-8")

    assert "`fallback_chain`" in text
    assert "`selected_source`" in text
