# Rename to pyqauto Report

Date: 2026-06-18

## Result

- PyPI package name: `pyqauto`
- Python import package: `pyqauto`
- CLI command: `pyqauto`
- Version: `0.3.0`
- GitHub repository: `https://github.com/tabman2026/pyqauto`
- GitHub Release: `https://github.com/tabman2026/pyqauto/releases/tag/v0.3.0`

## Completed

- Confirmed `pyqauto` had no matching PyPI distribution before release.
- Renamed GitHub repository to `tabman2026/pyqauto`.
- Updated `origin` to `https://github.com/tabman2026/pyqauto.git`.
- Renamed package directory from the old import package to `pyqauto`.
- Updated `pyproject.toml` to `name = "pyqauto"` and `version = "0.3.0"`.
- Updated console script to `pyqauto = "pyqauto.cli:main"`.
- Updated code imports, tests, examples, docs, scripts, and GitHub templates.
- Added `docs/MIGRATION_FROM_AQUOTE_ROUTER.md`.
- Deleted old `dist/` and rebuilt only `pyqauto-0.3.0` artifacts.
- Used GitHub Actions Trusted Publishing workflow; local PyPI upload was not used.

## Validation

- `python -X utf8 -m pytest -q`: PASS
- `python -X utf8 -m ruff check .`: PASS
- `python -X utf8 scripts/check_release.py`: PASS
- `python -X utf8 scripts/smoke_test.py`: PASS
- `python -X utf8 -m build`: PASS

Built artifacts:

```text
dist/pyqauto-0.3.0.tar.gz
dist/pyqauto-0.3.0-py3-none-any.whl
```

## Publish Status

GitHub Actions Publish run `27712370388` built the package but failed at PyPI
Trusted Publishing with `invalid-publisher`. PyPI publication is blocked until
the PyPI Pending Publisher is configured for `pyqauto`.

## Audit Conclusion

This task only changes naming, package metadata, docs, tests, and release
configuration. It does not add investment advice, screening, timing signal
generation, account login, order execution, or performance promise behavior.

## Acceptance Result

Accepted for code rename, local validation, GitHub repository rename, tag, and
GitHub Release. PyPI publication and post-release cold-start installation are
blocked by missing PyPI Pending Publisher configuration.

