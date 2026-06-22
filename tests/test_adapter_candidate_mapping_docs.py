from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ROOT / "docs" / "ADAPTER_CANDIDATE_REVIEW_V040.md",
    ROOT / "docs" / "ADAPTER_FIELD_MAPPING_DRAFT_V040.md",
    ROOT / "docs" / "ADAPTER_UNIT_RULES_DRAFT_V040.md",
    ROOT / "docs" / "SOURCE_POLICY_DRAFT_V040.md",
]


def _candidate_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in DOCS)


def test_adapter_candidate_mapping_doc_covers_required_mappings() -> None:
    text = (ROOT / "docs" / "ADAPTER_FIELD_MAPPING_DRAFT_V040.md").read_text(
        encoding="utf-8"
    )
    for heading in [
        "efinance Realtime -> pyqauto QuoteRecord",
        "efinance Kline -> pyqauto KlineBar",
        "baostock Kline -> pyqauto KlineBar",
        "mootdx Quote -> pyqauto QuoteRecord",
        "mootdx Kline -> pyqauto KlineBar",
    ]:
        assert heading in text
    for header in ["上游字段", "上游含义", "上游单位", "标准字段", "缺失处理"]:
        assert header in text


def test_adapter_candidate_docs_do_not_present_candidates_as_formal_support() -> None:
    text = _candidate_text()
    assert "已正式支持" not in text
    assert "not officially supported" in text
    assert "not part of the default fallback chain" in text


def test_adapter_candidate_docs_avoid_forbidden_scope_and_local_paths() -> None:
    text = _candidate_text()
    forbidden = [
        "Q" + "MT",
        "券" + "商",
        "真实" + "交易",
        "候选股" + "池",
        "买卖" + "点",
        "收益" + "率",
        "胜" + "率",
    ]
    for term in forbidden:
        assert term not in text
    for path_marker in ["C:" + "\\Users", "Desktop" + "/CODEX"]:
        assert path_marker not in text
