"""Probe pytdx server availability and write a local active pool."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aquote_router.adapters.base import code_for_symbol, market_for_symbol  # noqa: E402
from aquote_router.adapters.pytdx_adapter import (  # noqa: E402
    PYTDX_KLINE_PERIOD_CATEGORIES,
)

DEFAULT_EXAMPLE_CONFIG = ROOT / "config" / "pytdx_servers.example.json"
DEFAULT_LOCAL_CONFIG = ROOT / "config" / "pytdx_servers.local.json"
DEFAULT_ACTIVE_CONFIG = ROOT / "config" / "pytdx_servers.active.local.json"
DEFAULT_SYMBOL = "000001"
DEFAULT_MINUTE_PERIOD = "15m"
DEFAULT_COUNT = 10
DEFAULT_TIMEOUT = 2.0
DEFAULT_WORKERS = 8
DEFAULT_ACTIVE_COUNT = 10
ROLE_SEQUENCE = ("primary", "hot_backup", "hot_backup")


@dataclass(frozen=True)
class ServerCandidate:
    host: str
    port: int
    source: str
    role: str = "backup"
    configured_latency_ms: int = 999999
    enabled: bool = True
    name: str | None = None

    def key(self) -> tuple[str, int]:
        return (self.host, self.port)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Probe pytdx servers and generate a local active server pool."
    )
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    parser.add_argument(
        "--example-config",
        default=_display_path(DEFAULT_EXAMPLE_CONFIG),
        help="Project example server config, resolved relative to the repository root.",
    )
    parser.add_argument(
        "--local-config",
        default=_display_path(DEFAULT_LOCAL_CONFIG),
        help="Optional local server config, resolved relative to the repository root.",
    )
    parser.add_argument(
        "--active-config",
        default=_display_path(DEFAULT_ACTIVE_CONFIG),
        help="Generated active local config, resolved relative to the repository root.",
    )
    parser.add_argument("--symbol", default=DEFAULT_SYMBOL)
    parser.add_argument(
        "--minute-period",
        choices=[period for period in PYTDX_KLINE_PERIOD_CATEGORIES if period != "1d"],
        default=DEFAULT_MINUTE_PERIOD,
    )
    parser.add_argument("--count", default=DEFAULT_COUNT, type=int)
    parser.add_argument("--timeout", default=DEFAULT_TIMEOUT, type=float)
    parser.add_argument("--workers", default=DEFAULT_WORKERS, type=int)
    parser.add_argument("--active-count", default=DEFAULT_ACTIVE_COUNT, type=int)
    parser.add_argument(
        "--limit",
        default=None,
        type=int,
        help="Optional diagnostic limit after loading and de-duplicating candidates.",
    )
    args = parser.parse_args()

    example_config = _resolve_repo_path(args.example_config)
    local_config = _resolve_repo_path(args.local_config)
    active_config = _resolve_repo_path(args.active_config)

    started_at = datetime.now(timezone.utc)
    official_candidates, official_sources, pytdx_import_error = _load_official_pytdx_servers()
    example_total_count, example_candidates = _load_config_candidates(
        example_config,
        source=_display_path(example_config),
        optional=False,
    )
    local_total_count, local_candidates = _load_config_candidates(
        local_config,
        source=_display_path(local_config),
        optional=True,
    )
    candidates = _dedupe_candidates(
        [*official_candidates, *example_candidates, *local_candidates]
    )
    if args.limit is not None:
        candidates = candidates[: max(args.limit, 0)]

    results = _probe_candidates(
        candidates,
        timeout=max(args.timeout, 0.1),
        workers=max(args.workers, 1),
        symbol=args.symbol,
        minute_period=args.minute_period,
        count=max(args.count, 1),
    )
    sorted_results = sorted(results, key=_result_sort_key)
    active_entries = _build_active_config(sorted_results, active_count=max(args.active_count, 0))
    _write_json(active_config, active_entries)

    finished_at = datetime.now(timezone.utc)
    summary = _build_summary(
        started_at=started_at,
        finished_at=finished_at,
        pytdx_import_error=pytdx_import_error,
        official_sources=official_sources,
        official_candidates=official_candidates,
        example_total_count=example_total_count,
        local_total_count=local_total_count,
        candidates=candidates,
        results=sorted_results,
        active_config=active_config,
        active_entries=active_entries,
        symbol=args.symbol,
        minute_period=args.minute_period,
        count=max(args.count, 1),
        timeout=max(args.timeout, 0.1),
        workers=max(args.workers, 1),
    )

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(
            "Pytdx probe finished: "
            f"{summary['connect_success_count']}/{summary['probe_server_count']} "
            "servers connected. "
            f"Active config: {summary['active_config_path']}"
        )
    return 0


def _load_official_pytdx_servers() -> tuple[list[ServerCandidate], list[dict[str, Any]], str | None]:
    candidates: list[ServerCandidate] = []
    sources: list[dict[str, Any]] = []
    import_error: str | None = None

    try:
        from pytdx.config.hosts import hq_hosts
    except Exception as exc:  # pragma: no cover - depends on user environment
        import_error = f"{type(exc).__name__}: {exc}"
        hq_hosts = []

    hq_count = 0
    for item in hq_hosts:
        candidate = _candidate_from_hq_host(item)
        if candidate:
            hq_count += 1
            candidates.append(candidate)
    sources.append(
        {
            "module": "pytdx.config.hosts",
            "object": "hq_hosts",
            "candidate_count": hq_count,
        }
    )

    try:
        from pytdx.util.best_ip import stock_ip
    except Exception:
        stock_ip = []

    stock_count = 0
    for item in stock_ip:
        candidate = _candidate_from_stock_ip(item)
        if candidate:
            stock_count += 1
            candidates.append(candidate)
    sources.append(
        {
            "module": "pytdx.util.best_ip",
            "object": "stock_ip",
            "candidate_count": stock_count,
        }
    )

    return _dedupe_candidates(candidates), sources, import_error


def _candidate_from_hq_host(item: Any) -> ServerCandidate | None:
    if not isinstance(item, (list, tuple)) or len(item) < 3:
        return None
    name, host, port = item[0], item[1], item[2]
    return _candidate_from_values(
        host=host,
        port=port,
        source="pytdx.config.hosts.hq_hosts",
        name=str(name) if name is not None else None,
    )


def _candidate_from_stock_ip(item: Any) -> ServerCandidate | None:
    if not isinstance(item, dict):
        return None
    return _candidate_from_values(
        host=item.get("ip"),
        port=item.get("port"),
        source="pytdx.util.best_ip.stock_ip",
        name=str(item.get("name")) if item.get("name") is not None else None,
    )


def _candidate_from_values(
    *,
    host: Any,
    port: Any,
    source: str,
    role: str = "backup",
    latency_ms: Any = 999999,
    enabled: Any = True,
    name: str | None = None,
) -> ServerCandidate | None:
    try:
        host_text = str(host).strip()
        port_int = int(port)
        latency_int = int(latency_ms)
    except (TypeError, ValueError):
        return None
    if not host_text or port_int <= 0:
        return None
    role_text = str(role)
    if role_text not in {"primary", "hot_backup", "backup"}:
        role_text = "backup"
    return ServerCandidate(
        host=host_text,
        port=port_int,
        source=source,
        role=role_text,
        configured_latency_ms=latency_int,
        enabled=bool(enabled),
        name=name,
    )


def _load_config_candidates(
    path: Path,
    *,
    source: str,
    optional: bool,
) -> tuple[int, list[ServerCandidate]]:
    if not path.exists():
        if optional:
            return 0, []
        raise FileNotFoundError(f"pytdx server config not found: {_display_path(path)}")

    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError(f"pytdx server config must be a JSON list: {_display_path(path)}")

    candidates: list[ServerCandidate] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        if not bool(item.get("enabled", True)):
            continue
        candidate = _candidate_from_values(
            host=item.get("host"),
            port=item.get("port", 7709),
            source=source,
            role=item.get("role", "backup"),
            latency_ms=item.get("latency_ms", 999999),
            enabled=item.get("enabled", True),
        )
        if candidate:
            candidates.append(candidate)
    return len(raw), candidates


def _dedupe_candidates(candidates: list[ServerCandidate]) -> list[ServerCandidate]:
    deduped: list[ServerCandidate] = []
    seen: set[tuple[str, int]] = set()
    for candidate in candidates:
        key = candidate.key()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)
    return deduped


def _probe_candidates(
    candidates: list[ServerCandidate],
    *,
    timeout: float,
    workers: int,
    symbol: str,
    minute_period: str,
    count: int,
) -> list[dict[str, Any]]:
    if not candidates:
        return []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                _probe_candidate,
                candidate,
                timeout=timeout,
                symbol=symbol,
                minute_period=minute_period,
                count=count,
            )
            for candidate in candidates
        ]
        return [future.result() for future in concurrent.futures.as_completed(futures)]


def _probe_candidate(
    candidate: ServerCandidate,
    *,
    timeout: float,
    symbol: str,
    minute_period: str,
    count: int,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "host": candidate.host,
        "port": candidate.port,
        "source": candidate.source,
        "configured_role": candidate.role,
        "configured_latency_ms": candidate.configured_latency_ms,
        "name": candidate.name,
        "connect_success": False,
        "realtime_quote_success": False,
        "minute_kline_success": False,
        "daily_kline_success": False,
        "kline_success": False,
        "latency_ms": None,
        "total_latency_ms": None,
        "realtime_quote_count": 0,
        "minute_kline_count": 0,
        "daily_kline_count": 0,
        "errors": {},
    }
    started = time.perf_counter()
    api = None
    try:
        from pytdx.hq import TdxHq_API
    except Exception as exc:  # pragma: no cover - depends on user environment
        result["errors"]["import"] = _error_text(exc)
        return result

    try:
        api = TdxHq_API(heartbeat=True, auto_retry=False)
        connect_started = time.perf_counter()
        connected = api.connect(candidate.host, candidate.port, time_out=timeout)
        result["latency_ms"] = round((time.perf_counter() - connect_started) * 1000, 3)
        result["connect_success"] = bool(connected)
        if not connected:
            result["errors"]["connect"] = "connect returned false"
            return result

        _probe_realtime(api, result, symbol)
        _probe_minute_kline(api, result, symbol, minute_period, count)
        _probe_daily_kline(api, result, symbol, count)
        result["kline_success"] = bool(
            result["minute_kline_success"] or result["daily_kline_success"]
        )
        return result
    except Exception as exc:
        result["errors"].setdefault("connect", _error_text(exc))
        return result
    finally:
        result["total_latency_ms"] = round((time.perf_counter() - started) * 1000, 3)
        if api is not None:
            try:
                api.disconnect()
            except Exception:
                pass


def _probe_realtime(api: Any, result: dict[str, Any], symbol: str) -> None:
    try:
        rows = api.get_security_quotes([(market_for_symbol(symbol), code_for_symbol(symbol))])
        count = len(rows or [])
        result["realtime_quote_count"] = count
        result["realtime_quote_success"] = count > 0
        if count == 0:
            result["errors"]["realtime_quote"] = "empty response"
    except Exception as exc:
        result["errors"]["realtime_quote"] = _error_text(exc)


def _probe_minute_kline(
    api: Any,
    result: dict[str, Any],
    symbol: str,
    period: str,
    count: int,
) -> None:
    try:
        rows = api.get_security_bars(
            PYTDX_KLINE_PERIOD_CATEGORIES[period],
            market_for_symbol(symbol),
            code_for_symbol(symbol),
            0,
            count,
        )
        row_count = len(rows or [])
        result["minute_kline_count"] = row_count
        result["minute_kline_success"] = row_count > 0
        if row_count == 0:
            result["errors"]["minute_kline"] = "empty response"
    except Exception as exc:
        result["errors"]["minute_kline"] = _error_text(exc)


def _probe_daily_kline(api: Any, result: dict[str, Any], symbol: str, count: int) -> None:
    try:
        rows = api.get_security_bars(
            PYTDX_KLINE_PERIOD_CATEGORIES["1d"],
            market_for_symbol(symbol),
            code_for_symbol(symbol),
            0,
            count,
        )
        row_count = len(rows or [])
        result["daily_kline_count"] = row_count
        result["daily_kline_success"] = row_count > 0
        if row_count == 0:
            result["errors"]["daily_kline"] = "empty response"
    except Exception as exc:
        result["errors"]["daily_kline"] = _error_text(exc)


def _result_sort_key(result: dict[str, Any]) -> tuple[Any, ...]:
    latency = result["latency_ms"] if result["latency_ms"] is not None else 999999999
    minute_success = bool(result["minute_kline_success"])
    daily_success = bool(result["daily_kline_success"])
    return (
        not bool(result["connect_success"]),
        not (minute_success and daily_success),
        not (minute_success or daily_success),
        not bool(result["realtime_quote_success"]),
        latency,
        str(result["host"]),
        int(result["port"]),
    )


def _build_active_config(
    sorted_results: list[dict[str, Any]],
    *,
    active_count: int,
) -> list[dict[str, Any]]:
    if active_count <= 0:
        return []
    useful = [
        result
        for result in sorted_results
        if result["connect_success"]
        and (
            result["realtime_quote_success"]
            or result["minute_kline_success"]
            or result["daily_kline_success"]
        )
    ]
    if not useful:
        useful = [result for result in sorted_results if result["connect_success"]]
    entries: list[dict[str, Any]] = []
    for index, result in enumerate(useful[:active_count]):
        latency_ms = result["latency_ms"] if result["latency_ms"] is not None else 999999
        entries.append(
            {
                "host": result["host"],
                "port": int(result["port"]),
                "role": _role_for_index(index),
                "latency_ms": int(round(float(latency_ms))),
                "enabled": True,
            }
        )
    return entries


def _role_for_index(index: int) -> str:
    if index < len(ROLE_SEQUENCE):
        return ROLE_SEQUENCE[index]
    return "backup"


def _build_summary(
    *,
    started_at: datetime,
    finished_at: datetime,
    pytdx_import_error: str | None,
    official_sources: list[dict[str, Any]],
    official_candidates: list[ServerCandidate],
    example_total_count: int,
    local_total_count: int,
    candidates: list[ServerCandidate],
    results: list[dict[str, Any]],
    active_config: Path,
    active_entries: list[dict[str, Any]],
    symbol: str,
    minute_period: str,
    count: int,
    timeout: float,
    workers: int,
) -> dict[str, Any]:
    connect_success_count = _count_success(results, "connect_success")
    realtime_success_count = _count_success(results, "realtime_quote_success")
    minute_success_count = _count_success(results, "minute_kline_success")
    daily_success_count = _count_success(results, "daily_kline_success")
    return {
        "task": "018.1",
        "mode": "pytdx_server_pool_probe",
        "created_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_seconds": round((finished_at - started_at).total_seconds(), 3),
        "probe_parameters": {
            "symbol": symbol,
            "minute_period": minute_period,
            "count": count,
            "timeout": timeout,
            "workers": workers,
        },
        "pytdx_package_import_error": pytdx_import_error,
        "official_pytdx_sources": official_sources,
        "official_pool_count": len(official_candidates),
        "original_pool_count": example_total_count,
        "local_pool_count": local_total_count,
        "probe_server_count": len(candidates),
        "connect_success_count": connect_success_count,
        "realtime_quote_success_count": realtime_success_count,
        "minute_kline_success_count": minute_success_count,
        "daily_kline_success_count": daily_success_count,
        "fastest_available_server": _fastest_available_server(results),
        "active_config_generated": active_config.exists(),
        "active_config_path": _display_path(active_config),
        "active_config_server_count": len(active_entries),
        "results": results,
    }


def _count_success(results: list[dict[str, Any]], key: str) -> int:
    return sum(1 for result in results if result.get(key))


def _fastest_available_server(results: list[dict[str, Any]]) -> dict[str, Any] | None:
    useful = [
        result
        for result in results
        if result["connect_success"]
        and (
            result["realtime_quote_success"]
            or result["minute_kline_success"]
            or result["daily_kline_success"]
        )
    ]
    if not useful:
        useful = [result for result in results if result["connect_success"]]
    if not useful:
        return None
    fastest = sorted(useful, key=_result_sort_key)[0]
    return {
        "host": fastest["host"],
        "port": fastest["port"],
        "latency_ms": fastest["latency_ms"],
        "realtime_quote_success": fastest["realtime_quote_success"],
        "minute_kline_success": fastest["minute_kline_success"],
        "daily_kline_success": fastest["daily_kline_success"],
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _resolve_repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return ROOT / path


def _display_path(path: Path) -> str:
    try:
        relative = path.resolve().relative_to(ROOT.resolve())
    except (OSError, ValueError):
        return f"<external-path>/{path.name}"
    return str(relative).replace("\\", "/")


def _error_text(exc: Exception) -> str:
    return f"{type(exc).__name__}: {exc}"


if __name__ == "__main__":
    raise SystemExit(main())
