"""Significant-figures rounding and formatting: exact Decimal math, trailing zeros kept."""

from __future__ import annotations

from ._format import format_sig
from ._round import round_sig

__version__ = "0.1.0"

__all__ = ["format_sig", "round_sig"]
