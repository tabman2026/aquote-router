from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BEGINNER_DEVELOPER_GUIDE.md"
DOCS = [
    ROOT / "docs" / "BEGINNER_DEVELOPER_GUIDE.md",
    ROOT / "docs" / "UPSTREAM_COMMONS_RESEARCH.md",
    ROOT / "docs" / "ADAPTER_TEMPLATE.md",
    ROOT / "docs" / "FIELD_MAPPING_TEMPLATE.md",
    ROOT / "docs" / "UNIT_RULES_FOR_ADAPTERS.md",
    ROOT / "docs" / "WHEN_TO_RELEASE.md",
]
FORBIDDEN_TERMS = [
    "Q" + "MT",
    "券" + "商",
    "真实" + "交易",
    "候选" + "股池",
    "买卖" + "点",
    "收益" + "率",
    "胜" + "率",
    "to" + "ken",
    "coo" + "kie",
    "sec" + "ret",
    "web" + "hook",
    "C:" + "\\Users",
    "Desktop" + "/CODEX",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_beginner_developer_guide_exists() -> None:
    assert DOC.exists()


def test_beginner_developer_guide_mentions_adapter_methods() -> None:
    text = read(DOC)

    assert "fetch_raw" in text
    assert "normalize_to_standard" in text
    assert "validate_standard_output" in text


def test_readmes_link_developer_docs() -> None:
    readme = read(ROOT / "README.md")
    readme_zh = read(ROOT / "README.zh-CN.md")

    for doc in DOCS:
        rel = doc.relative_to(ROOT).as_posix()
        assert rel in readme
        assert rel in readme_zh


def test_new_docs_do_not_contain_forbidden_terms() -> None:
    for doc in DOCS:
        text = read(doc)
        for term in FORBIDDEN_TERMS:
            assert term not in text
