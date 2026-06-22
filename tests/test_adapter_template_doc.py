from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ADAPTER_TEMPLATE.md"


def test_adapter_template_doc_exists() -> None:
    assert DOC.exists()


def test_adapter_template_contains_required_methods() -> None:
    text = DOC.read_text(encoding="utf-8")

    for marker in [
        "source_name",
        "fetch_raw",
        "inspect_raw_schema",
        "normalize_to_standard",
        "validate_standard_output",
    ]:
        assert marker in text
