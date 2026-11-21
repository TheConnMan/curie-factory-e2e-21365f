"""Conversion table and the one function the CLI calls."""

from __future__ import annotations

LENGTH_TO_METERS = {
    "m": 1.0,
    "km": 1000.0,
    "mi": 1609.344,
    "ft": 0.3048,
}

TEMPERATURE = {"c", "f"}

DEFAULT_PRECISION = 2


class UnknownUnit(ValueError):
    """Raised when a unit is not in the table."""


def convert(value: float, src: str, dst: str, *, rounding: int | bool | None = None) -> float:
    """Convert ``value`` from unit ``src`` to unit ``dst``.

    Temperature and length units cannot be mixed.

    Pass ``rounding`` to get a rounded result instead of the raw float:
    ``True`` rounds to ``DEFAULT_PRECISION`` decimal places, an ``int``
    rounds to that many places, ``None`` or ``False`` (the default)
    returns the unrounded result. Rounding follows Python's built-in
    ``round`` (half to even) and applies to every conversion family,
    identity conversions included.
    """
    result = _raw_convert(value, src, dst)
    if rounding is None or rounding is False:
        return result
    digits = DEFAULT_PRECISION if rounding is True else rounding
    return round(result, digits)


def _raw_convert(value: float, src: str, dst: str) -> float:
    src = src.lower()
    dst = dst.lower()
    if src in TEMPERATURE and dst in TEMPERATURE:
        return _convert_temperature(value, src, dst)
    if src in LENGTH_TO_METERS and dst in LENGTH_TO_METERS:
        meters = value * LENGTH_TO_METERS[src]
        return meters / LENGTH_TO_METERS[dst]
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
