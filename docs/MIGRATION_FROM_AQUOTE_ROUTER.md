# Migration From aquote-router

This project has been renamed to `pyqauto`.

## Name Changes

Old install command:

```bash
pip install aquote-router
```

New install command:

```bash
pip install pyqauto
```

Old Python import:

```python
from aquote_router import QuoteRouter
```

New Python import:

```python
from pyqauto import QuoteRouter
```

Old CLI command:

```bash
aquote-router kline 000001 --period 15m
```

New CLI command:

```bash
pyqauto kline 000001 --period 15m
```

## Compatibility Policy

The original `aquote-router` package is not deleted at this time, but new users
should install and import `pyqauto`.

Functionality is unchanged under the new name:

- realtime quotes
- minute K-line
- daily K-line
- unified `kline`
- `probe-pytdx`
- `diagnose`
- source policy
- JSONL and SQLite audit trail

If the old GitHub repository has already been renamed, GitHub may redirect old
links automatically. New documentation only recommends:

```text
https://github.com/tabman2026/pyqauto
```

## Boundary

`pyqauto` remains a market data source selection and audit tool. It does not
provide investment advice, screening, timing signals, account login, order
execution, or performance promises.
