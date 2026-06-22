from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_DRAFT = ROOT / "docs" / "SOURCE_POLICY_DRAFT_V040.md"


def test_adapter_candidate_policy_draft_keeps_candidates_disabled() -> None:
    text = POLICY_DRAFT.read_text(encoding="utf-8")
    assert "Candidate adapters are not directly enabled" in text
    assert "Do not directly enable candidate adapter entries from this draft" in text
    assert "方案 B 不能直接启用" in text


def test_adapter_candidate_policy_draft_does_not_use_easyquotation_for_kline() -> None:
    text = POLICY_DRAFT.read_text(encoding="utf-8")
    assert "Do not use easyquotation as a K-line fallback" in text
    assert "daily_kline:\n  pytdx -> efinance or baostock" in text
    assert "minute_kline:\n  pytdx -> efinance or baostock" in text
    assert "daily_kline:\n  pytdx -> easyquotation" not in text
    assert "minute_kline:\n  pytdx -> easyquotation" not in text
