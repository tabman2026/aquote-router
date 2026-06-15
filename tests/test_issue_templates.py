from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"


def test_required_issue_templates_exist() -> None:
    for name in [
        "bug_report.yml",
        "data_source_failure.yml",
        "adapter_request.yml",
        "docs_issue.yml",
    ]:
        assert (TEMPLATE_DIR / name).exists()


def test_issue_templates_request_trace_and_diagnose_json() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in TEMPLATE_DIR.glob("*.yml")
    )

    for field in [
        "aquote-router version",
        "Python version",
        "Operating system",
        "command",
        "API name",
        "symbol",
        "period/count",
        "trace_id",
        "diagnose --json output",
        "probe-pytdx output",
        "Sanitized audit log snippet",
    ]:
        assert field in combined

    assert "trace_id" in combined
    assert "diagnose --json" in combined


def test_data_source_failure_template_has_required_fields() -> None:
    text = (TEMPLATE_DIR / "data_source_failure.yml").read_text(encoding="utf-8")

    for field in [
        "aquote-router version",
        "Python version",
        "Operating system",
        "Executed command",
        "Stock symbol",
        "API name",
        "period / count",
        "trace_id",
        "Sanitized audit log snippet",
        "diagnose --json output",
        "probe-pytdx output",
        "outside trading hours",
        "Can you reproduce it?",
    ]:
        assert field in text
