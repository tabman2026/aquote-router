# PyPI Trusted Publishing Setup

Configure PyPI Trusted Publishing for this project before attempting PyPI publication.

- PyPI project name: `pyqauto`
- GitHub owner: `tabman2026`
- GitHub repository: `pyqauto`
- Workflow file: `publish.yml`
- Environment: `pypi`
- Release tag: `v0.3.0`

The workflow uses GitHub OIDC Trusted Publishing and does not require storing PyPI credentials in the repository.

Current status: GitHub repository rename to `tabman2026/pyqauto` is complete. PyPI publication for `pyqauto` 0.3.0 must use GitHub Actions Trusted Publishing with the `pypi` environment.
