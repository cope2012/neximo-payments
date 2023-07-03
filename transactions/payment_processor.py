from typing import List, Dict


_IVA = 1.16
_COMMISSION = 1.03
_EXEMPT_AMOUNT = 500
USD_TO_MXN = 17
_USD_CURRENCY = "USD"


def _maybe_convert_to_mxn(payment: Dict, partial) -> None:
    currency = payment["currency"]
    amount = payment["amount"]

    if currency == _USD_CURRENCY:
        partial["total"] = amount * USD_TO_MXN
    else:
        partial["total"] = amount


def _get_taxes(partial: Dict) -> None:
    amount = partial['total']

    if amount >= _EXEMPT_AMOUNT:
        total = amount / _IVA
        partial["total"] = total
        partial["taxes"] = amount - total


def _get_commission(partial: Dict) -> None:
    amount = partial["total"]
    total = amount / _COMMISSION
    partial["commission"] = amount - total
    partial["total"] = total


def _normalize_response(resp: Dict) -> None:
    resp['taxes'] = round(resp['taxes'], 2)
    resp['total'] = round(resp['total'], 2)
    resp['commission'] = round(resp['commission'], 2)


def process_payments(payments: List[Dict]) -> Dict:
    resp = {
        "total": 0,
        "taxes": 0,
        "commission": 0,
    }

    for payment in payments:
        partial = {
            "total": 0,
            "taxes": 0,
            "commission": 0
        }

        _maybe_convert_to_mxn(payment, partial)
        if payment['currency'] == _USD_CURRENCY:
            _get_commission(partial)
        _get_taxes(partial)

        resp["total"] += partial["total"]
        resp["taxes"] += partial["taxes"]
        resp["commission"] += partial["commission"]

    _normalize_response(resp)

    return resp
