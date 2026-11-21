"""Conversion table and the one function the CLI calls."""

from __future__ import annotations

LENGTH_TO_METERS = {
    "m": 1.0,
    "km": 1000.0,
    "mi": 1609.344,
    "ft": 0.3048,
}

TEMPERATURE = {"c", "f", "r"}


class UnknownUnit(ValueError):
    """Raised when a unit is not in the table."""


def convert(value: float, src: str, dst: str) -> float:
    """Convert ``value`` from unit ``src`` to unit ``dst``.

    Temperature and length units cannot be mixed.
    """
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


_TO_CELSIUS = {
    "c": lambda value: value,
    "f": lambda value: (value - 32) * 5 / 9,
    "r": lambda value: (value - 491.67) * 5 / 9,
}

_FROM_CELSIUS = {
    "c": lambda value: value,
    "f": lambda value: value * 9 / 5 + 32,
    "r": lambda value: (value + 273.15) * 9 / 5,
}


def _convert_temperature(value: float, src: str, dst: str) -> float:
    if src == dst:
        return value
    celsius = _TO_CELSIUS[src](value)
    return _FROM_CELSIUS[dst](celsius)
