"""Significant-figures rounding and formatting: exact Decimal math, trailing zeros kept."""

from __future__ import annotations

from ._count import count_sig, sig_bounds
from ._errors import (
    AmbiguousFiguresError,
    InvalidFiguresError,
    InvalidNumberError,
    InvalidOptionError,
    SigFigsError,
    UncertaintyError,
)
from ._format import format_sig
from ._modes import NOTATIONS, ROUNDING_MODES, Notation, Rounding
from ._round import Number, round_decimal, round_sig
from ._uncertainty import STYLES, Style, format_uncertainty, round_uncertainty

__version__ = "0.2.0"

__all__ = [
    "NOTATIONS",
    "ROUNDING_MODES",
    "STYLES",
    "AmbiguousFiguresError",
    "InvalidFiguresError",
    "InvalidNumberError",
    "InvalidOptionError",
    "Notation",
    "Number",
    "Rounding",
    "SigFigsError",
    "Style",
    "UncertaintyError",
    "count_sig",
    "format_sig",
    "format_uncertainty",
    "round_decimal",
    "round_sig",
    "round_uncertainty",
    "sig_bounds",
]
