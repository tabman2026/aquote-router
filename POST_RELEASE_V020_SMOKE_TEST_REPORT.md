# Post-release v0.2.0 Smoke Test Report

Date: 2026-06-15

## Release Targets

- GitHub Release: https://github.com/tabman2026/pyqauto/releases/tag/v0.2.0
- PyPI project: https://pypi.org/project/pyqauto/
- PyPI version verified: `0.2.0`

## Checks

| Check | Result |
|---|---|
| PyPI index lists `0.2.0` | PASS |
| Fresh venv created for verification | PASS |
| `pip install pyqauto -i https://pypi.org/simple` installs `0.2.0` | PASS |
| `import pyqauto; print(pyqauto.__version__)` | PASS |
| `from pyqauto import QuoteRouter` | PASS |
| `pyqauto --help` | PASS |
| `pyqauto minute --help` | PASS |
| `pyqauto daily --help` | PASS |
| `pyqauto kline --help` | PASS |
| `pyqauto diagnose --json` | PASS |

## Notes

Validation commands were run from outside the repository directory to avoid local
source shadowing. `diagnose --json` ran successfully and reported missing default
config files in the external working directory, which is expected for this
verification mode.
