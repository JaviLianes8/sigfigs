"""Exact significant-figures rounding built on decimal.Decimal."""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal, DecimalException, localcontext

Number = int | float | str | Decimal


def _to_decimal(x: Number) -> Decimal:
    if isinstance(x, bool):
        raise TypeError("booleans are not valid numbers")
    if isinstance(x, Decimal):
        value = x
    elif isinstance(x, int):
        value = Decimal(x)
    elif isinstance(x, float):
        value = Decimal(str(x))
    elif isinstance(x, str):
        try:
            value = Decimal(x)
        except DecimalException as error:
            raise ValueError(f"not a number: {x!r}") from error
    else:
        raise TypeError(f"unsupported type: {type(x).__name__}")
    if not value.is_finite():
        raise ValueError("cannot round a non-finite number")
    return value


def _check_figures(figures: int) -> None:
    if isinstance(figures, bool) or not isinstance(figures, int):
        raise TypeError("figures must be an int")
    if figures < 1:
        raise ValueError("figures must be at least 1")


def round_to_decimal(x: Number, figures: int) -> Decimal:
    """Round to the given significant figures, half to even, as an exact Decimal."""
    _check_figures(figures)
    value = _to_decimal(x)
    if value == 0:
        return Decimal(0)
    with localcontext() as ctx:
        ctx.prec = figures + 3
        ctx.rounding = ROUND_HALF_EVEN
        quantum = Decimal(1).scaleb(value.adjusted() - (figures - 1))
        rounded = value.quantize(quantum)
        if rounded.adjusted() != value.adjusted():
            quantum = Decimal(1).scaleb(rounded.adjusted() - (figures - 1))
            rounded = value.quantize(quantum)
    return rounded


def round_sig(x: Number, figures: int) -> float:
    """Round x to the given number of significant figures and return a float."""
    return float(round_to_decimal(x, figures))
