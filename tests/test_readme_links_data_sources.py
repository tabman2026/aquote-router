from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_links_core_docs() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    for doc_name in [
        "docs/QUICKSTART.md",
        "docs/NEW_USER_START_HERE.md",
        "docs/API_REFERENCE.md",
        "docs/KLINE_GUIDE.md",
        "docs/DATA_SOURCES.md",
        "docs/ISSUE_GUIDE.md",
        "docs/RETURN_FIELDS.md",
        "docs/CLI_REFERENCE.md",
        "docs/TROUBLESHOOTING.md",
        "docs/ERROR_CODES.md",
        "docs/SYMBOL_RULES.md",
        "docs/UNITS.md",
        "docs/MAINTAINER_CHECKLIST.md",
    ]:
        assert doc_name in readme
