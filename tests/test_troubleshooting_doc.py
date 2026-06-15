from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_maintenance_docs_exist() -> None:
    for name in [
        "TROUBLESHOOTING.md",
        "ERROR_CODES.md",
        "SYMBOL_RULES.md",
        "TIME_AND_TRADING_DAY.md",
        "UNITS.md",
        "UPSTREAM_LICENSE_AND_RISK.md",
        "ROADMAP.md",
        "CONTRIBUTOR_ADAPTER_GUIDE.md",
    ]:
        assert (ROOT / "docs" / name).exists()


def test_troubleshooting_doc_exists_and_mentions_diagnostics() -> None:
    text = (ROOT / "docs" / "TROUBLESHOOTING.md").read_text(encoding="utf-8")

    assert "aquote-router diagnose" in text
    assert "aquote-router diagnose --json" in text
    assert "trace_id" in text
    assert "source_policy_parseable" in text
    assert "pytdx_server_config_parseable" in text


def test_docs_do_not_contain_blocked_terms() -> None:
    blocked_terms = [
        "Q" + "MT",
        "券" + "商",
        "真实" + "交易",
        "候选" + "股池",
        "买卖" + "点",
        "收益" + "率",
        "胜" + "率",
    ]
    docs_dir = ROOT / "docs"

    for path in docs_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for term in blocked_terms:
            assert term not in text, f"{term} found in {path.name}"
