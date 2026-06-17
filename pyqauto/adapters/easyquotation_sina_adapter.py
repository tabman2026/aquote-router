"""easyquotation Sina adapter."""

from __future__ import annotations

from typing import Any

from pyqauto.adapters.base import (
    BaseQuoteAdapter,
    as_float,
    code_for_symbol,
    first_value,
)
from pyqauto.exceptions import AdapterError, ErrorCode, SourceUnavailableError
from pyqauto.models import QuoteRecord


class EasyQuotationSinaAdapter(BaseQuoteAdapter):
    """Adapter for easyquotation's Sina provider."""

    source = "easyquotation_sina"
    provider = "sina"

    def realtime_quotes(
        self, symbols: list[str], *, include_raw: bool = False
    ) -> list[QuoteRecord]:
        return self._stocks(symbols, include_raw=include_raw)

    def full_realtime_quotes(
        self, symbols: list[str], *, include_raw: bool = False
    ) -> list[QuoteRecord]:
        return self._stocks(symbols, include_raw=include_raw)

    def index_realtime(
        self, symbols: list[str], *, include_raw: bool = False
    ) -> list[QuoteRecord]:
        return self._stocks(symbols, include_raw=include_raw)

    def _stocks(self, symbols: list[str], *, include_raw: bool) -> list[QuoteRecord]:
        if not symbols:
            return []

        normalized_symbols = [code_for_symbol(symbol) for symbol in symbols]
        quotation = self._quotation()
        data = quotation.stocks(normalized_symbols)
        if not data:
            raise SourceUnavailableError(
                f"{self.source} returned no quote records",
                code=_source_error_code(self.source),
            )

        records: list[QuoteRecord] = []
        for symbol in normalized_symbols:
            row = data.get(symbol) or data.get(symbol.lower()) or data.get(symbol.upper())
            if row:
                records.append(self._normalize(symbol, row, include_raw=include_raw))
        if not records:
            raise SourceUnavailableError(
                f"{self.source} returned no requested symbols",
                code=_source_error_code(self.source),
            )
        return records

    def _quotation(self) -> Any:
        try:
            import easyquotation
        except Exception as exc:  # pragma: no cover - depends on user env
            raise AdapterError("easyquotation package is not available") from exc
        return easyquotation.use(self.provider)

    def _normalize(
        self, symbol: str, row: dict[str, Any], *, include_raw: bool
    ) -> QuoteRecord:
        date_value = first_value(row, ("date",))
        time_value = first_value(row, ("time",))
        if date_value and time_value:
            dt_value = f"{date_value} {time_value}"
        else:
            dt_value = str(first_value(row, ("datetime", "time")) or "") or None

        return QuoteRecord(
            symbol=symbol,
            name=first_value(row, ("name",)),
            price=as_float(first_value(row, ("now", "price", "close"))),
            open=as_float(first_value(row, ("open",))),
            high=as_float(first_value(row, ("high",))),
            low=as_float(first_value(row, ("low",))),
            pre_close=as_float(first_value(row, ("close", "pre_close", "last_close"))),
            volume=as_float(first_value(row, ("volume", "vol"))),
            amount=as_float(first_value(row, ("turnover", "amount"))),
            datetime=dt_value,
            source=self.source,
            source_level=self.source_level,
            raw=dict(row) if include_raw else None,
        )


def _source_error_code(source: str) -> ErrorCode:
    if source == "easyquotation_tencent":
        return ErrorCode.EASYQUOTATION_TENCENT_FAILED
    return ErrorCode.EASYQUOTATION_SINA_FAILED
