from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_diagnose_help_can_run() -> None:
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "aquote_router.cli", "diagnose", "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )

    assert result.returncode == 0
    assert "--json" in result.stdout


def test_diagnose_json_can_run_and_has_required_fields() -> None:
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "aquote_router.cli", "diagnose", "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)

    for key in [
        "aquote_router_version",
        "python_version",
        "os",
        "config_files",
        "source_policy_parseable",
        "pytdx_server_config_parseable",
        "enabled_sources",
        "supported_apis",
        "supported_kline_periods",
        "audit_output_paths",
        "recent_trace_id",
    ]:
        assert key in payload
    assert payload["config_files"]["source_policy"]["exists"] is True
    assert payload["source_policy_parseable"] is True
    assert payload["pytdx_server_config_parseable"] is True
    assert "minute_kline" in payload["supported_apis"]
    assert "1m" in payload["supported_kline_periods"]

    output = result.stdout.lower()
    blocked_paths = ["c:" + "\\users", "/" + "users" + "/", "desktop" + "/codex"]
    for blocked in blocked_paths:
        assert blocked not in output
