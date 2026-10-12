"""Exception types. Every error a caller can fix is a ``SigFigsError``, itself a ``ValueError``."""

from __future__ import annotations


class SigFigsError(ValueError):
    """Base class for every value error raised by sigfigs.

    It subclasses ``ValueError`` so code written against 0.1.0, which raised plain
    ``ValueError``, keeps catching everything.
    """


class InvalidNumberError(SigFigsError):
    """The input is not a finite number: unparsable text, NaN or infinity."""


class InvalidFiguresError(SigFigsError):
    """The requested count of significant figures is below one."""


class InvalidOptionError(SigFigsError):
    """An option such as ``rounding``, ``notation`` or ``style`` has an unknown value."""


class AmbiguousFiguresError(SigFigsError):
    """A strict count met trailing zeros that may or may not be significant (``"1200"``)."""


class UncertaintyError(SigFigsError):
    """The uncertainty is zero or negative, so it cannot set a rounding position."""
