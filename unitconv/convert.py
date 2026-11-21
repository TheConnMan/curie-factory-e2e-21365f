"""Conversion table and the one function the CLI calls."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, localcontext

LENGTH_TO_METERS = {
    "m": 1.0,
    "km": 1000.0,
    "mi": 1609.344,
    "ft": 0.3048,
}

TEMPERATURE = {"c", "f"}


class UnknownUnit(ValueError):
    """Raised when a unit is not in the table."""


def convert(
    value: float,
    src: str,
    dst: str,
    *,
    round_result: bool = False,
    round_digits: int = 2,
) -> float:
    """Convert ``value`` from unit ``src`` to unit ``dst``.

    Temperature and length units cannot be mixed.

    With ``round_result=True`` the result is rounded half up to
    ``round_digits`` decimal places (default 2).
    """
    src = src.lower()
    dst = dst.lower()
    result: float
    if src in TEMPERATURE and dst in TEMPERATURE:
        result = _convert_temperature(value, src, dst)
    elif src in LENGTH_TO_METERS and dst in LENGTH_TO_METERS:
        meters = value * LENGTH_TO_METERS[src]
        result = meters / LENGTH_TO_METERS[dst]
    elif src not in TEMPERATURE and src not in LENGTH_TO_METERS:
        raise UnknownUnit(src)
    elif dst not in TEMPERATURE and dst not in LENGTH_TO_METERS:
        raise UnknownUnit(dst)
    else:
        raise ValueError(f"cannot convert {src} to {dst}")
    if round_result:
        return _round_half_up(result, round_digits)
    return result


def _round_half_up(value: float, digits: int) -> float:
    """Round ``value`` half up to ``digits`` decimal places."""
    text = str(value)
    with localcontext() as context:
        # Enough precision for every integer digit of ``value`` plus the
        # requested decimal places, so large values and large ``digits``
        # do not hit the default context's 28-digit limit.
        context.prec = max(28, Decimal(text).adjusted() + 1 + digits + 2)
        rounded = Decimal(text).quantize(
            Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP
        )
    return float(rounded)


def _convert_temperature(value: float, src: str, dst: str) -> float:
    if src == dst:
        return value
    if src == "c":
        return value * 9 / 5 + 32
    return (value - 32) * 5 / 9
