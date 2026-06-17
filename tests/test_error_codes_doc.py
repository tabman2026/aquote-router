from __future__ import annotations

from pathlib import Path

from pyqauto.exceptions import ERROR_CODES

ROOT = Path(__file__).resolve().parents[1]


def test_error_codes_doc_exists_and_lists_all_codes() -> None:
    path = ROOT / "docs" / "ERROR_CODES.md"
    text = path.read_text(encoding="utf-8")

    for code in ERROR_CODES:
        assert f"`{code}`" in text
    assert "Meaning" in text
    assert "Typical cause" in text


def test_readme_links_core_maintenance_docs() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    for doc_name in [
        "TROUBLESHOOTING.md",
        "ERROR_CODES.md",
        "DATA_SOURCES.md",
        "KLINE_GUIDE.md",
    ]:
        assert doc_name in readme
