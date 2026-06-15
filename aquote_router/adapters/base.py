"""Base adapter contracts and shared helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aquote_router.exceptions import AdapterError, UnsupportedSymbolError
from aquote_router.models import KlineBar, QuoteRecord


@dataclass(frozen=True)
class PytdxServer:
    """One pytdx server configuration entry."""

    host: str
    port: int
    role: str
    latency_ms: int
    enabled: bool = True


@dataclass(frozen=True)
class NormalizedSymbol:
    """Provider-ready symbol code and pytdx market id."""

    code: str
    market: int
    suffix: str | None = None


class BaseQuoteAdapter:
    """Synchronous quote adapter interface."""

    source: str = "unknown"
    source_level: str | None = None

    def realtime_quotes(
        self, symbols: list[str], *, include_raw: bool = False
    ) -> list[QuoteRecord]:
        raise AdapterError(f"{self.source} does not support realtime_quotes")

    def full_realtime_quotes(
        self, symbols: list[str], *, include_raw: bool = False
    ) -> list[QuoteRecord]:
        return self.realtime_quotes(symbols, include_raw=include_raw)

    def index_realtime(
        self, symbols: list[str], *, include_raw: bool = False
    ) -> list[QuoteRecord]:
        return self.realtime_quotes(symbols, include_raw=include_raw)

    def minute_kline(
        self,
        symbol: str,
        *,
        period: str = "1m",
        count: int = 240,
        include_raw: bool = False,
    ) -> list[KlineBar]:
        raise AdapterError(f"{self.source} does not support minute_kline")

    def daily_kline(
        self,
        symbol: str,
        *,
        count: int = 120,
        include_raw: bool = False,
    ) -> list[KlineBar]:
        raise AdapterError(f"{self.source} does not support daily_kline")


def as_float(value: Any) -> float | None:
    """Best-effort conversion to float with empty values mapped to None."""

    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def first_value(row: dict[str, Any], keys: tuple[str, ...]) -> Any:
    """Return the first present value for a tuple of candidate keys."""

    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def market_for_symbol(symbol: str) -> int:
    """Return pytdx market id for a common A-share symbol."""

    return normalize_symbol(symbol).market


def code_for_symbol(symbol: str) -> str:
    """Return the six-digit provider code for a documented symbol."""

    return normalize_symbol(symbol).code


def normalize_symbol(symbol: str) -> NormalizedSymbol:
    """Normalize documented A-share symbol forms.

    Supported forms are six digits and six digits followed by .SH or .SZ.
    Bare 6/5/9 prefixes use Shanghai, while bare 0/3 prefixes use Shenzhen.
    """

    raw = str(symbol or "").strip().upper()
    if "." in raw:
        code, separator, suffix = raw.partition(".")
        if separator != "." or suffix not in {"SH", "SZ"}:
            raise UnsupportedSymbolError(f"unsupported symbol suffix: {symbol}")
        if not _is_six_digit_code(code):
            raise UnsupportedSymbolError(f"unsupported symbol code: {symbol}")
        return NormalizedSymbol(code=code, market=1 if suffix == "SH" else 0, suffix=suffix)

    if not _is_six_digit_code(raw):
        raise UnsupportedSymbolError(f"unsupported symbol code: {symbol}")
    if raw.startswith(("5", "6", "9")):
        return NormalizedSymbol(code=raw, market=1)
    if raw.startswith(("0", "3")):
        return NormalizedSymbol(code=raw, market=0)
    raise UnsupportedSymbolError(f"unsupported symbol prefix: {symbol}")


def source_id(source: str, source_level: str | None) -> str:
    """Return a compact source identifier for fallback chains."""

    if source_level:
        return f"{source}:{source_level}"
    return source


def _is_six_digit_code(value: str) -> bool:
    return len(value) == 6 and value.isdigit()
