# Upstream Commons Research

This document records the upstream review behind the pyqauto adapter rules. It
is a research note, not an implementation promise. Only features already present
in pyqauto are described as supported.

## Scope

Reviewed upstreams:

| Upstream | Official material read | Focus |
|---|---|---|
| AKShare | https://akshare.akfamily.xyz/ and https://github.com/akfamily/akshare | `stock_zh_a_spot_em`, `stock_zh_a_hist`, `stock_zh_a_hist_min_em`, field tables, unit notes, changelog |
| efinance | https://efinance.readthedocs.io/ and https://github.com/Micro-sheep/efinance | `ef.stock.get_realtime_quotes`, `ef.stock.get_quote_history`, `klt`, `fqt`, returned fields |
| pytdx | https://github.com/rainx/pytdx and https://rainx.gitbooks.io/pytdx/content/ | `get_security_quotes`, `get_security_bars`, market and category values, connect and failover behavior |
| easyquotation | https://github.com/shidenggui/easyquotation | `easyquotation.use("sina")`, `easyquotation.use("tencent")`, realtime fields, Sina/Tencent shape differences |
| baostock | https://www.baostock.com/ and official package metadata/source from https://pypi.org/project/baostock/ | `login`, `logout`, `query_history_k_data_plus`, `frequency`, `adjustflag`, returned fields |
| mootdx | https://github.com/mootdx/mootdx and https://mootdx.readthedocs.io/ | pytdx wrapping, best server probing, CLI, friendlier quote API |

Note: the baostock public home page did not expose a readable API page during
this review. The official PyPI page and official source package were used to
verify function signatures and examples.

## Upstream Positioning

| Upstream | Positioning | Suitable pyqauto role | Not suitable role | Primary? | Fallback? | v0.4.0 adapter plan |
|---|---|---|---|---|---|---|
| AKShare | Broad public financial data interface with many A-share endpoints. | Existing realtime fallback via Eastmoney spot; optional K-line candidate only after adapter tests. | Sole primary source; unvalidated raw passthrough. | No. | Yes for realtime after schema guard. | Optional expansion candidate. |
| efinance | Eastmoney-oriented public data library returning DataFrame objects. | Optional adapter candidate for realtime and K-line research after unit tests. | Default primary source without drift guard. | No. | Possible after tests. | Candidate. |
| pytdx | TDX protocol client with explicit server connection and bar category values. | Current primary for realtime and all pyqauto K-line APIs. | Guaranteed always-on source. | Yes, as current policy. | Yes across configured pytdx servers. | Keep and harden. |
| easyquotation | Sina/Tencent realtime quote wrapper. | Existing realtime fallback for Sina and Tencent. | K-line fallback. | No. | Yes for realtime only. | Keep realtime fallback only. |
| baostock | Historical data client with login/session flow and ResultData paging. | Optional historical adapter candidate after mock tests and live probe. | Realtime source. | No. | Possible for historical APIs if policy later allows. | Candidate. |
| mootdx | Friendlier wrapper around tdxpy/pytdx-style access with best server probing and CLI. | Reference for pyqauto `probe-pytdx` ergonomics and optional adapter candidate. | Replacement for pyqauto policy/audit layer. | No. | Possible only as optional adapter. | Reference plus candidate. |

## Confirmed Interface Notes

| Upstream | Confirmed APIs | Return shape | Important parameters |
|---|---|---|---|
| AKShare | `stock_zh_a_spot_em`, `stock_zh_a_hist`, `stock_zh_a_hist_min_em` | Mostly pandas DataFrame. | `symbol`, `period`, `start_date`, `end_date`, `adjust` depend on endpoint. |
| efinance | `ef.stock.get_realtime_quotes`, `ef.stock.get_quote_history` | DataFrame for one symbol; dict of DataFrame for multiple history symbols. | `fs`, `beg`, `end`, `klt`, `fqt`, `market_type`. |
| pytdx | `get_security_quotes`, `get_security_bars` | list, convertible through `api.to_df`. | `market`, `category`, `stockcode`, `start`, `count`. |
| easyquotation | `easyquotation.use("sina")`, `easyquotation.use("tencent")`, `real`, `market_snapshot` | dict keyed by symbol. | `prefix`, symbol list, channel name. |
| baostock | `login`, `logout`, `query_history_k_data_plus` | ResultData cursor; examples build DataFrame from `fields`. | `code`, `fields`, `start_date`, `end_date`, `frequency`, `adjustflag`. |
| mootdx | `Quotes.factory`, `quotes`, `bars`, `index`, `minute`, CLI `bestip` | pandas DataFrame or None. | `market`, `bestip`, `timeout`, `frequency`, `offset`. |

## Common Findings

1. Most upstream sources are public convenience libraries, not official exchange
   authorized realtime feeds.
2. Most Python financial data sources return pandas DataFrame, dict, list, or a
   custom cursor-like object.
3. Field names are not unified. Common examples include `最新价`, `price`,
   `close`, `now`, `开盘`, `open`, `最高`, `high`, `最低`, `low`, `成交量`,
   `volume`, `成交额`, and `amount`.
4. Units are not unified. Volume may be in lots or shares. Amount may be yuan or
   ten-thousand-yuan. Percent-like fields are usually displayed as percent
   numbers, but each adapter must verify this.
5. Symbol formats differ: `000001`, `000001.SZ`, `sz000001`, and `SH.600000`
   all appear in common Python data libraries.
6. K-line period parameters differ: `1m`, `5m`, `15m`, `30m`, `60m`, `1d`;
   integers such as `1`, `5`, `15`, `30`, `60`, `101`; pytdx category numbers;
   and baostock `frequency` strings.
7. Adjustment parameters differ: `qfq`, `hfq`, empty string, `fqt`, `adjust`,
   `adjustflag`, and English words such as `none`, `forward`, `backward`.
8. Free public sources can fail because of delay, throttling, field drift,
   connection refusal, remote close, empty payloads, or server timeout.
9. pyqauto therefore keeps the path as `adapter -> normalize -> validate ->
   audit -> public record`.
10. Data that fails standard field validation must not enter public records.

## Differences By Topic

### 字段命名差异 / Field Naming

| Concept | AKShare | efinance | pytdx/mootdx | easyquotation | baostock | pyqauto standard |
|---|---|---|---|---|---|---|
| Symbol | `代码` | `股票代码` | `code` or request code | dict key or prefixed code | `code` | `symbol` |
| Name | `名称` | `股票名称` | `name` when available | `name` | field-selected | `name` |
| Last price | `最新价` or `收盘` | `最新价` or `收盘` | `price`/bar close | `now` or `price` | `close` | `price` for quote, `close` for bar |
| Previous close | `昨收` or `pre_close` | `昨日收盘` or `preclose` | provider field when available | `close` | `preclose` | `pre_close` |
| Volume | `成交量` | `成交量` | `vol`/`amount` naming varies by API | `turnover` or composite field | `volume` | `volume_shares` |
| Amount | `成交额` | `成交额` | provider field | `volume` or composite field | `amount` | `amount_yuan` |

### 单位差异 / Unit Rules

| Upstream | Observed unit risk | pyqauto handling |
|---|---|---|
| AKShare | Eastmoney spot `成交量` is lots; `成交额` is yuan. | lots multiplied by 100 into `volume_shares`; amount kept as `amount_yuan`. |
| efinance | Examples show `成交量` and `成交额`; unit must be confirmed per endpoint before admission. | Require adapter `unit_rules` and tests before any public record. |
| pytdx | Bar and quote numeric fields vary by security type and endpoint. | Current adapter normalizes only documented A-share records. |
| easyquotation | Sina exposes simple fields; Tencent can expose a composite price/lot-volume/yuan-amount field. | Composite fields must be parsed before validation. |
| baostock | Official examples expose `volume` and `amount`; unit must be verified in adapter tests before acceptance. | Optional adapter must declare unit rules. |
| mootdx | Wraps tdxpy/pytdx-like output and returns DataFrame. | Treat as pytdx-family raw data, not automatically standard. |

### 股票代码格式差异 / Symbol Format

| Upstream | Common input/output forms |
|---|---|
| AKShare | often six-digit `symbol`; returned `代码` may be plain six digits. |
| efinance | plain six digits, names, or market-specific query IDs in raw output. |
| pytdx | `(market, "000001")` where market is `0` for Shenzhen and `1` for Shanghai. |
| easyquotation | `000001`, `sh000001`, `sz000001`, `bj` prefix when requested. |
| baostock | `sh.600000`, `sz.000001`; source code accepts some reversed forms. |
| mootdx | plain six-digit symbol plus derived market. |

### K线周期参数差异 / K-line Period Parameters

| Upstream | Period style |
|---|---|
| AKShare | `period` strings such as daily/minute variants, endpoint-specific. |
| efinance | `klt`: `1`, `5`, `15`, `30`, `60`, `101`, `102`, `103`. |
| pytdx | category: `0` 5m, `1` 15m, `2` 30m, `3` 60m, `4` daily, `5` weekly, `6` monthly, `7`/`8` 1m, `9` daily, `10` quarterly, `11` yearly. |
| easyquotation | Realtime A-share quote wrapper; do not use as pyqauto K-line fallback. |
| baostock | `frequency`: examples confirm `d` and `5`; official examples also separate minute, week, and month field sets. |
| mootdx | `frequency` is converted to pytdx-style category before calling bars. |

### 复权参数差异 / Adjustment Parameters

| Upstream | Adjustment style |
|---|---|
| AKShare | `adjust` values are endpoint-specific, commonly empty, `qfq`, `hfq`. |
| efinance | `fqt`: `0` no adjustment, `1` forward, `2` backward. |
| pytdx | Raw bars are not a full adjustment abstraction in pyqauto today. |
| easyquotation | Not applicable to realtime quote fallback. |
| baostock | `adjustflag`: official examples show `3` no adjustment and `2` forward adjustment. |
| mootdx | Follows tdxpy/pytdx-family bar behavior. |

### 返回结构差异 / Return Structures

| Shape | Upstreams |
|---|---|
| pandas DataFrame | AKShare, efinance, mootdx; baostock examples build one from ResultData. |
| dict | easyquotation realtime. |
| list | pytdx raw quote/bar responses. |
| custom cursor/result | baostock `ResultData`. |

### 失败模式差异 / Failure Modes

| Upstream | Failure modes to model |
|---|---|
| AKShare | endpoint repair churn, field changes, empty DataFrame, remote errors. |
| efinance | invalid `fs` can raise KeyError; search/cache behavior can match unexpected symbols; remote failures. |
| pytdx | connect false, returned None, server timeout, broken connection, failover exhaustion. |
| easyquotation | empty dict, channel-specific fields, remote response shape change. |
| baostock | not logged in, parameter error, non-zero `error_code`, network receive error. |
| mootdx | best server probe failure, empty DataFrame, tdxpy exceptions, timeout. |

## Adapter Implications

Every new adapter must:

1. Fetch raw data through public upstream APIs only.
2. Record raw schema shape without storing private auth material.
3. Declare field mapping and unit rules.
4. Normalize symbols, periods, amount, volume, source, source level, and
   `trace_id`.
5. Validate standard records before they can leave the adapter boundary.
6. Write audit attempts and rejected reasons.
7. Add offline tests before any live probe.
8. Update docs when source policy, fields, or audit shape changes.

## v0.4.0 Notes

- Keep pytdx as the current primary for K-line APIs.
- Keep easyquotation as realtime-only fallback.
- Treat AKShare, efinance, baostock, and mootdx expansions as optional adapter
  work that requires mock tests, field normalization tests, live probe support,
  and source policy review.
- Do not add a K-line fallback unless the upstream returns compatible period,
  adjustment, timestamp, volume, and amount semantics and passes validation.

v0.4.0 adapter 候选评审入口：

- [ADAPTER_CANDIDATE_REVIEW_V040.md](ADAPTER_CANDIDATE_REVIEW_V040.md)
- [ADAPTER_FIELD_MAPPING_DRAFT_V040.md](ADAPTER_FIELD_MAPPING_DRAFT_V040.md)
- [ADAPTER_UNIT_RULES_DRAFT_V040.md](ADAPTER_UNIT_RULES_DRAFT_V040.md)
- [SOURCE_POLICY_DRAFT_V040.md](SOURCE_POLICY_DRAFT_V040.md)

These are candidate adapter review documents only. They do not mean the current
version supports efinance, baostock, or mootdx as runtime data sources.
