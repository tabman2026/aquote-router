# Contributor Adapter Guide

New real data adapters require tests before code is accepted.

Required checks:

- Adapter unit tests with mocked upstream responses.
- Field normalization tests for every returned public field.
- Source policy tests.
- Audit tests that verify attempts and `fallback_chain`.
- Documentation updates for API reference, data sources, return fields, units,
  and source policy.

Default tests must not require network access. Live smoke tests must be guarded
by `ENABLE_LIVE_SMOKE_TEST=1`.

Adapters must call public APIs only and must not embed private credentials or
account state.
