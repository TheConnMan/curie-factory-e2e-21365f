"""Conversion table and the one function the CLI calls."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP, localcontext

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
    rounded: bool = False,
    precision: int = 2,
) -> float:
    """Convert ``value`` from unit ``src`` to unit ``dst``.

    Temperature and length units cannot be mixed.

    With ``rounded=True`` the result is rounded half up (half away from
    zero) to ``precision`` decimal places (default 2); without it the
    raw float is returned.
    """
    src = src.lower()
    dst = dst.lower()
    if src in TEMPERATURE and dst in TEMPERATURE:
        result = _convert_temperature(value, src, dst)
    elif src in LENGTH_TO_METERS and dst in LENGTH_TO_METERS:
        meters = value * LENGTH_TO_METERS[src]
        result = meters / LENGTH_TO_METERS[dst]
    else:
        if src not in TEMPERATURE and src not in LENGTH_TO_METERS:
            raise UnknownUnit(src)
        if dst not in TEMPERATURE and dst not in LENGTH_TO_METERS:
            raise UnknownUnit(dst)
        raise ValueError(f"cannot convert {src} to {dst}")
    if not rounded:
        return result
    return _round_half_up(result, precision)


def _round_half_up(value: float, precision: int) -> float:
    """Round half away from zero to ``precision`` decimal places."""
    decimal_value = Decimal(str(value)) if value >= 0 else -Decimal(str(-value))
    with localcontext() as ctx:
        # The default 28-digit context raises InvalidOperation when the
        # result's magnitude plus the requested precision exceeds it
        # (e.g. 1e26, or precision=30); size the context to the value.
        ctx.prec = max(28, decimal_value.adjusted() + 1 + max(precision, 0) + 2)
        exponent = Decimal(1).scaleb(-precision)
        return float(decimal_value.quantize(exponent, rounding=ROUND_HALF_UP))


def _convert_temperature(value: float, src: str, dst: str) -> float:
    if src == dst:
        return value
    if src == "c":
        return value * 9 / 5 + 32
    return (value - 32) * 5 / 9
