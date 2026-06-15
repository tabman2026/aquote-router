from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_return_fields_mentions_source_fields() -> None:
    text = (ROOT / "docs" / "RETURN_FIELDS.md").read_text(encoding="utf-8")

    for field in ["source", "source_level", "fallback_from", "is_fallback", "trace_id"]:
        assert f"`{field}`" in text
    assert "KlineBar" in text
