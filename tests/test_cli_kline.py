from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "pyqauto.cli", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )


def test_cli_kline_help_can_start() -> None:
    for command in ["realtime", "full", "full-realtime", "index", "minute", "daily", "kline"]:
        result = run_cli(command, "--help")
        assert result.returncode == 0, result.stderr
        assert "--json" in result.stdout or command == "full-realtime"


def test_cli_unsupported_kline_period_returns_nonzero() -> None:
    result = run_cli("kline", "000001", "--period", "2m", "--json")

    assert result.returncode != 0
    assert "UNSUPPORTED_PERIOD" in result.stderr
