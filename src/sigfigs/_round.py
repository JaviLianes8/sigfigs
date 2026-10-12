"""Exact significant-figures rounding built on decimal.Decimal."""

from __future__ import annotations

from decimal import MAX_EMAX, MIN_EMIN, Context, Decimal, DecimalException, Underflow

from ._errors import InvalidFiguresError, InvalidNumberError
from ._modes import Rounding, decimal_mode

MAX_FIGURES = 10_000
"""Largest accepted count of significant figures; larger counts raise InvalidFiguresError."""

Number = int | float | str | Decimal
"""Accepted numeric input. Floats are read through ``repr``, the shortest round-trip text."""


def to_decimal(x: Number) -> Decimal:
    """Convert an accepted input to a finite Decimal without any binary rounding."""
    if isinstance(x, bool):
        raise TypeError("booleans are not valid numbers")
    if isinstance(x, Decimal):
        value = x
    elif isinstance(x, int):
        value = Decimal(x)
    elif isinstance(x, float):
        value = Decimal(repr(x))
    elif isinstance(x, str):
        try:
            value = Decimal(x.strip())
        except DecimalException as error:
            raise InvalidNumberError(f"not a number: {x!r}") from error
    else:
        raise TypeError(f"unsupported type: {type(x).__name__}")
    if not value.is_finite():
        raise InvalidNumberError(f"not a finite number: {x!r}")
    return value


def check_figures(figures: int, name: str = "figures") -> None:
    """Reject a figures count that is not an int from 1 to ``MAX_FIGURES``."""
    if isinstance(figures, bool) or not isinstance(figures, int):
        raise TypeError(f"{name} must be an int")
    if not 1 <= figures <= MAX_FIGURES:
        raise InvalidFiguresError(f"{name} must be from 1 to {MAX_FIGURES}, got {figures}")


def exact_context(digits: int, rounding: str) -> Context:
    """A context that traps overflow, underflow and invalid operations."""
    ctx = Context(prec=digits, rounding=rounding, Emax=MAX_EMAX, Emin=MIN_EMIN)
    ctx.traps[Underflow] = True
    return ctx


def out_of_range(x: object) -> InvalidNumberError:
    """The error for a value whose exponent leaves the representable decimal range."""
    return InvalidNumberError(f"exponent out of range: {x!r}")


def round_value(value: Decimal, figures: int, rounding: str) -> Decimal:
    """Round a finite Decimal to ``figures`` digits with a ``decimal`` rounding constant.

    The result always carries exactly ``figures`` coefficient digits, so its exponent
    records which digits are significant. Zero becomes a positive zero with
    ``figures - 1`` decimal places, matching how ``format_sig`` writes it.
    """
    ctx = exact_context(figures, rounding)
    if value.is_zero():
        return Decimal(0).scaleb(1 - figures, ctx)
    try:
        rounded = ctx.plus(value)
        quantum = Decimal(1).scaleb(rounded.adjusted() - figures + 1, ctx)
        return rounded.quantize(quantum, context=ctx)
    except DecimalException:
        raise out_of_range(value) from None


def round_decimal(x: Number, figures: int, *, rounding: Rounding = "half_even") -> Decimal:
    """Round ``x`` to ``figures`` significant figures and return an exact Decimal.

    The exponent of the result records the significant figures, so trailing zeros survive:

    >>> round_decimal(1.2, 3)
    Decimal('1.20')
    >>> round_decimal(123456, 2)
    Decimal('1.2E+5')
    >>> round_decimal("2.5", 1, rounding="half_up")
    Decimal('3')

    ``rounding`` is one of ``ROUNDING_MODES``; the default ``"half_even"`` is the rule of
    NIST SP 811 B.7.1 and the IEEE 754 default. Floats are read through ``repr`` (so
    ``2.675`` is the decimal 2.675, not its binary neighbour).

    Raises:
        TypeError: ``x`` or ``figures`` has an unsupported type.
        InvalidNumberError: ``x`` is unparsable text, NaN, infinite, or so large or
            small that its exponent leaves the decimal range.
        InvalidFiguresError: ``figures`` is below one or above ``MAX_FIGURES``.
        InvalidOptionError: ``rounding`` is not a known mode.
    """
    check_figures(figures)
    mode = decimal_mode(rounding)
    return round_value(to_decimal(x), figures, mode)


def round_sig(x: Number, figures: int, *, rounding: Rounding = "half_even") -> float:
    """Round ``x`` to ``figures`` significant figures and return a float.

    >>> round_sig(123456, 3)
    123000.0
    >>> round_sig(2.675, 3)
    2.68
    >>> round_sig(0.0125, 2, rounding="half_up")
    0.013

    The rounding itself is exact decimal arithmetic; only the final conversion to
    ``float`` is binary, so a result beyond the float range becomes ``inf`` or ``0.0``.
    Use ``round_decimal`` to keep the exact result.
    Raises the same errors as ``round_decimal``.
    """
    return float(round_decimal(x, figures, rounding=rounding))
