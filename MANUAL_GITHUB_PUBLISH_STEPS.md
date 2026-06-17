# Manual GitHub Publish Steps

Use these steps if the GitHub CLI is unavailable or not authenticated.

```bash
git remote add origin https://github.com/<owner>/pyqauto.git
git branch -M main
git push -u origin main
git push origin v0.3.0
```

Then create or confirm a public GitHub repository named `pyqauto`, add topics from the README, and create a release for tag `v0.3.0` using `CHANGELOG.md`.
