"""easyquotation Tencent adapter."""

from pyqauto.adapters.easyquotation_sina_adapter import EasyQuotationSinaAdapter


class EasyQuotationTencentAdapter(EasyQuotationSinaAdapter):
    """Adapter for easyquotation's Tencent provider."""

    source = "easyquotation_tencent"
    provider = "tencent"
