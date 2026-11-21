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
    digits: int = 2,
) -> float:
    """Convert ``value`` from unit ``src`` to unit ``dst``.

    Temperature and length units cannot be mixed.

    With ``rounded=True`` the result is rounded half up (ties away from
    zero) to ``digits`` decimal places, two by default.
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
    if rounded:
        return _round_half_up(result, digits)
    return result


def _round_half_up(value: float, digits: int) -> float:
    quantum = Decimal("1").scaleb(-digits)
    with localcontext() as ctx:
        # Floats carry at most ~309 integer digits (|value| < 2**1024), so
        # digits + 400 always covers the quantized result's coefficient.
        ctx.prec = digits + 400
        return float(Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP))
    if src not in TEMPERATURE and src not in LENGTH_TO_METERS:
        raise UnknownUnit(src)
    if dst not in TEMPERATURE and dst not in LENGTH_TO_METERS:
        raise UnknownUnit(dst)
    raise ValueError(f"cannot convert {src} to {dst}")


def _convert_temperature(value: float, src: str, dst: str) -> float:
    if src == dst:
        return value
    if src == "c":
        return value * 9 / 5 + 32
    return (value - 32) * 5 / 9
