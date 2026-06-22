from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "FIELD_MAPPING_TEMPLATE.md"


def test_field_mapping_template_doc_exists() -> None:
    assert DOC.exists()


def test_field_mapping_template_contains_required_headers() -> None:
    text = DOC.read_text(encoding="utf-8")

    for marker in ["上游字段", "标准字段", "标准单位", "缺失处理"]:
        assert marker in text


def test_field_mapping_template_contains_standard_fields() -> None:
    text = DOC.read_text(encoding="utf-8")

    for marker in [
        "symbol",
        "name",
        "price",
        "open",
        "high",
        "low",
        "pre_close",
        "volume_shares",
        "amount_yuan",
        "datetime",
        "period",
        "source",
        "source_level",
        "trace_id",
        "raw",
    ]:
        assert marker in text
