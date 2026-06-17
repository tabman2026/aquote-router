# Post-release v0.2.1 Smoke Test Report

Date: 2026-06-15

## Release Targets

- GitHub Release: https://github.com/tabman2026/pyqauto/releases/tag/v0.2.1
- PyPI project: https://pypi.org/project/pyqauto/
- PyPI version verified: `0.2.1`

## Checks

| Check | Result |
|---|---|
| GitHub Actions `Publish` for `v0.2.1` | PASS |
| PyPI index lists `0.2.1` | PASS |
| Fresh venv created for verification | PASS |
| `pip install --upgrade pyqauto -i https://pypi.org/simple` installs `0.2.1` | PASS |
| `import pyqauto; print(pyqauto.__version__)` | PASS |
| `from pyqauto import QuoteRouter` | PASS |
| `pyqauto --help` | PASS |
| `pyqauto probe-pytdx --help` | PASS |
| `pyqauto kline --help` | PASS |
| `pyqauto diagnose --json` | PASS |

## Notes

Validation commands were run from outside the repository directory to avoid local
source shadowing. `diagnose --json` ran successfully and reported missing default
config files in the external working directory, which is expected for this
verification mode.

The first PyPI install attempt occurred before the simple index exposed
`0.2.1`, so it installed `0.2.0`. The publish workflow logs showed PyPI upload
responses of `200 OK`; a subsequent PyPI index query listed `0.2.1`, and the
verification venv was upgraded from official PyPI to `0.2.1` before the CLI
checks above were run.

## Acceptance

- Audit conclusion: v0.2.1 GitHub Release, PyPI publication, and cold-start CLI
  verification completed.
- Boundary conclusion: no trading integration, no account login, no screening or
  timing workflow, no return promise, and no investment advice workflow was
  added.
- K-line conclusion: K-line APIs remain pytdx-only and do not use easyquotation
  fallback.
