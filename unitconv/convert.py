"""Conversion table and the one function the CLI calls."""

from __future__ import annotations

LENGTH_TO_METERS = {
    "m": 1.0,
    "km": 1000.0,
    "mi": 1609.344,
    "ft": 0.3048,
}

TEMPERATURE = {"c", "f", "r", "de"}


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


def _convert_temperature(value: float, src: str, dst: str) -> float:
    if src == dst:
        return value
    if src == "c" and dst == "f":
        return value * 9 / 5 + 32
    if src == "f" and dst == "c":
        return (value - 32) * 5 / 9
    if src == "c" and dst == "r":
        return (value + 273.15) * 9 / 5
    if src == "r" and dst == "c":
        return value * 5 / 9 - 273.15
    if src == "f" and dst == "r":
        return value + 459.67
    if src == "r" and dst == "f":
        return value - 459.67
    if src == "c" and dst == "de":
        return (100 - value) * 3 / 2
    if src == "de" and dst == "c":
        return 100 - value * 2 / 3
    if src == "f" and dst == "de":
        return (100 - (value - 32) * 5 / 9) * 3 / 2
    if src == "de" and dst == "f":
        return (100 - value * 2 / 3) * 9 / 5 + 32
    if src == "r" and dst == "de":
        return (100 - (value * 5 / 9 - 273.15)) * 3 / 2
    if src == "de" and dst == "r":
        return (100 - value * 2 / 3 + 273.15) * 9 / 5
    raise ValueError(f"unsupported temperature pair {src} to {dst}")
