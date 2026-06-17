# PyPI Trusted Publishing Setup for pyqauto

GitHub Actions Publish failed for `v0.3.0` because PyPI returned
`invalid-publisher`. Do not use local twine upload, do not create `.pypirc`,
and do not request or store PyPI tokens.

Configure a Pending Publisher in the PyPI backend with these exact values:

```text
Project name: pyqauto
Owner: tabman2026
Repository name: pyqauto
Workflow name: publish.yml
Environment name: pypi
```

Observed GitHub Actions claims:

```text
Repository: tabman2026/pyqauto
Workflow file: .github/workflows/publish.yml
Ref: refs/tags/v0.3.0
Environment: pypi
```

After the Pending Publisher is configured, rerun the failed Publish workflow
for run `27712370388` from GitHub Actions. The workflow should publish
`pyqauto` 0.3.0 through Trusted Publishing.

