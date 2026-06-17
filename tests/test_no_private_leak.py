from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_scan_has_no_violations() -> None:
    spec = importlib.util.spec_from_file_location(
        "check_release", ROOT / "scripts" / "check_release.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.collect_violations(ROOT) == []


def test_readme_contains_required_boundary() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "does not provide investment advice" in readme
    assert "does not produce market data" in readme
    assert "K-line APIs never fall back to easyquotation" in readme


def test_pyproject_package_names() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert 'name = "pyqauto"' in pyproject
    assert 'pyqauto = "pyqauto.cli:main"' in pyproject


def test_cli_can_start() -> None:
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "pyqauto.cli", "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )

    assert result.returncode == 0
    assert "diagnose" in result.stdout
