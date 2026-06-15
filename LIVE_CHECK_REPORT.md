# Live Check Report

Created at: 2026-06-15T11:56:09.181857+00:00
Finished at: 2026-06-15T11:56:30.400710+00:00
Mode: live_check

This is a local manual diagnostic report. It is not part of GitHub Actions CI.
No trading, brokerage, account login, order placement, screening, timing,
return promise, or investment advice workflow is included.

## Acceptance

- Overall status: PASS
- Audit conclusion: JSONL and SQLite audit records were generated
- Requires v0.2.1: False
- K-line source rule: PASS

## Live Status

| Check | Status |
|---|---|
| realtime_quotes | PASS |
| full_realtime_quotes | PASS |
| index_realtime | PASS |
| minute_kline_1m | PASS |
| minute_kline_15m | PASS |
| minute_kline_60m | PASS |
| daily_kline | PASS |
| kline_15m | PASS |
| kline_1d | PASS |
| kline_unified | PASS |
| diagnose_json | PASS |

## Audit Outputs

- JSONL: `logs/live_check_audit.jsonl`
- SQLite: `logs/live_check_audit.sqlite3`
- JSONL records total: 50
- SQLite rows: {"quote_router_audit": 50, "quote_router_attempts": 285}
- All live API calls audited: True

## Results

| Kind | Check | Status | Rows | Sources | Trace IDs | Reason |
|---|---|---|---:|---|---|---|
| api | realtime_quotes(['000001', '600000', '399001']) | PASS | 3 | [{"source": "pytdx", "source_level": "primary"}] | efd54182096a4bb2afe613377c5b473c | live_source_ok |
| api | full_realtime_quotes(['000001', '600000', '399001']) | PASS | 3 | [{"source": "pytdx", "source_level": "primary"}] | 29483b0a5dd64912a09fa8ae034daf5a | live_source_ok |
| api | index_realtime(['399001']) | PASS | 1 | [{"source": "pytdx", "source_level": "primary"}] | e105c102100a49b5a49fe84ef53bd036 | live_source_ok |
| api | minute_kline(000001, period=1m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | 1e9b991a6e3345e682156329b477ad6b | live_source_ok |
| api | minute_kline(600000, period=1m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | e4c117899063495091ae89d69950cf66 | live_source_ok |
| api | minute_kline(399001, period=1m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | f78992b3bb1645a087a57de0f5db476b | live_source_ok |
| api | minute_kline(000001, period=15m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | be4c8580ad834e36a828ffbea98ccba0 | live_source_ok |
| api | minute_kline(600000, period=15m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | c3d5462aebab4385a46983c8be94708f | live_source_ok |
| api | minute_kline(399001, period=15m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | 4fc1d7a97d8f480d967d189023a559ea | live_source_ok |
| api | minute_kline(000001, period=60m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | 97474488a82049dd83861033bf8f68f4 | live_source_ok |
| api | minute_kline(600000, period=60m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | b30df6b042d240c08660bccc70bad90a | live_source_ok |
| api | minute_kline(399001, period=60m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | fab552e9ed4a42d0b5fa871366b1571f | live_source_ok |
| api | daily_kline(000001, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | eca0ff3326484a64994185ba787e26b0 | live_source_ok |
| api | daily_kline(600000, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | 9487eee1b8f844d9b0831cd582b9e6d9 | live_source_ok |
| api | daily_kline(399001, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | 27d251a1ab9b488e92db0db73089fc72 | live_source_ok |
| api | kline(000001, period=15m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | 6893bedff65d4624ab30ee11d7b1cc65 | live_source_ok |
| api | kline(600000, period=15m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | e9d679356d5f43bd9e78d8be99b39f49 | live_source_ok |
| api | kline(399001, period=15m, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | 044168f9d78845fea150e5980267d5c3 | live_source_ok |
| api | kline(000001, period=1d, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | d957b6b83f8947899926d290208605aa | live_source_ok |
| api | kline(600000, period=1d, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | 330999bbc70449fdbf02d30c5a6fa67d | live_source_ok |
| api | kline(399001, period=1d, count=10) | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | b89fa6798f9445fe8d8932b429d50d8e | live_source_ok |
| cli | aquote-router diagnose --json | PASS | 0 | [] |  | cli_ok |
| cli | aquote-router realtime 000001 600000 --json | PASS | 2 | [{"source": "pytdx", "source_level": "primary"}] | ec5d58aa755b4d7b9eeed54b82845803 | cli_ok |
| cli | aquote-router index 399001 --json | PASS | 1 | [{"source": "pytdx", "source_level": "primary"}] | ae88b619abc249e4871501e1e4aa3901 | cli_ok |
| cli | aquote-router kline 000001 --period 15m --count 10 --json | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | a76d1511c0284f518cc0803141dfe582 | cli_ok |
| cli | aquote-router kline 000001 --period 1d --count 10 --json | PASS | 10 | [{"source": "pytdx", "source_level": "primary"}] | 09fab7f466dc4f2b824a95959d2246b6 | cli_ok |

## Notes

- Realtime routing is checked through pytdx, then easyquotation Sina, then easyquotation Tencent.
- K-line checks are accepted only when returned rows report `source=pytdx`.
- Failed live source calls are recorded as diagnostic failures with the observed reason.
