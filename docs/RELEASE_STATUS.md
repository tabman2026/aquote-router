# Release Status

Version: `0.3.0`

Status: GitHub Release completed; PyPI publication blocked by Trusted Publishing setup.

Public URLs:

- GitHub repository: https://github.com/tabman2026/pyqauto
- GitHub Release: https://github.com/tabman2026/pyqauto/releases/tag/v0.3.0
- PyPI project: https://pypi.org/project/pyqauto/

Release gates:

- PyPI package name: `pyqauto`
- Python import package: `pyqauto`
- CLI command: `pyqauto`
- Publishing path: GitHub Actions Trusted Publishing
- Local twine upload: not allowed

Current blocker:

- Publish workflow run `27712370388` failed with `invalid-publisher`.
- Configure PyPI Pending Publisher for project `pyqauto`, then rerun the
  Publish workflow.
