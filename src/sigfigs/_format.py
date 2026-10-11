"""Render significant-figure values as strings while keeping trailing zeros."""

from __future__ import annotations

from decimal import Decimal

from ._round import Number, round_to_decimal


def _digits_and_exponent(rounded: Decimal) -> tuple[int, str, int]:
    sign, digits, exponent = rounded.as_tuple()
    assert isinstance(exponent, int)
    return sign, "".join(str(d) for d in digits), exponent


def _fixed(rounded: Decimal) -> str:
    sign, text, exponent = _digits_and_exponent(rounded)
    if exponent >= 0:
        body = text + "0" * exponent
    else:
        point = len(text) + exponent
        body = "0." + "0" * -point + text if point <= 0 else text[:point] + "." + text[point:]
    return "-" + body if sign else body


def _scientific(rounded: Decimal, figures: int) -> str:
    sign, text, exponent = _digits_and_exponent(rounded)
    text = text.ljust(figures, "0")
    power = exponent + len(text) - 1
    mantissa = text if figures == 1 else text[0] + "." + text[1:]
    marker = f"e{'+' if power >= 0 else '-'}{abs(power):02d}"
    return ("-" if sign else "") + mantissa + marker


def _zero(figures: int, sci: bool) -> str:
    mantissa = "0" if figures == 1 else "0." + "0" * (figures - 1)
    return mantissa + "e+00" if sci else mantissa


def format_sig(x: Number, figures: int, *, sci: bool = False) -> str:
    """Round x to the given significant figures and format it, keeping trailing zeros.

    Fixed notation by default (``1.20``), scientific when ``sci`` is true (``1.20e+00``).
    """
    rounded = round_to_decimal(x, figures)
    if rounded == 0:
        return _zero(figures, sci)
    return _scientific(rounded, figures) if sci else _fixed(rounded)
