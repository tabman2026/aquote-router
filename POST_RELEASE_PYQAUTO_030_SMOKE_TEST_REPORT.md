# Post-release pyqauto 0.3.0 Smoke Test Report

Date: 2026-06-18

## Status

Post-release cold-start smoke test was not executed because PyPI publication did
not complete.

## Blocking Reason

GitHub Actions Publish run `27712370388` failed with PyPI Trusted Publishing
`invalid-publisher`. PyPI needs a Pending Publisher configured for the new
project name `pyqauto`.

## Required Cold-start Commands After Publishing

```powershell
python -X utf8 -m venv .venv_pyqauto_check
.venv_pyqauto_check\Scripts\Activate.ps1
python -X utf8 -m pip install --upgrade pip
python -X utf8 -m pip install pyqauto -i https://pypi.org/simple
python -X utf8 -c "import pyqauto; print(pyqauto.__version__)"
python -X utf8 -c "from pyqauto import QuoteRouter; print(QuoteRouter)"
pyqauto --help
pyqauto diagnose --json
pyqauto probe-pytdx --help
pyqauto kline --help
```

## Audit Conclusion

Cold-start validation is blocked by publication state only. No local PyPI
upload, credential file, or password-based publishing path was used.

