# Time and Trading Day

The router does not calculate trading calendars. It preserves upstream timestamp
strings in `datetime`.

## Realtime APIs

`datetime` is built from upstream fields when available. Different upstream
providers may format this string differently.

## K-line APIs

`KlineBar.datetime` is the pytdx bar timestamp string. For daily bars, pytdx
typically returns a date-like value. For minute bars, pytdx typically returns a
date-time-like value.

Audit timestamps such as `started_at` and `finished_at` are UTC ISO-8601 strings.
