from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "WHEN_TO_RELEASE.md"


def test_when_to_release_doc_exists() -> None:
    assert DOC.exists()


def test_when_to_release_doc_contains_release_levels() -> None:
    text = DOC.read_text(encoding="utf-8")

    for marker in ["patch", "minor", "不发版本"]:
        assert marker in text
