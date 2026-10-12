"""Typed errors: each is a SigFigsError and still a ValueError, as in 0.1.0."""

import pytest

import sigfigs
from sigfigs import (
    AmbiguousFiguresError,
    InvalidFiguresError,
    InvalidNumberError,
    InvalidOptionError,
    SigFigsError,
    UncertaintyError,
    format_sig,
    round_decimal,
    round_sig,
)

ERRORS = [
    AmbiguousFiguresError,
    InvalidFiguresError,
    InvalidNumberError,
    InvalidOptionError,
    UncertaintyError,
]


@pytest.mark.parametrize("error", ERRORS)
def test_hierarchy(error: type[Exception]) -> None:
    assert issubclass(error, SigFigsError)
    assert issubclass(error, ValueError)


@pytest.mark.parametrize("text", ["abc", "", "1.2.3", "nan", "-inf", "Infinity", "sNaN"])
def test_invalid_numbers(text: str) -> None:
    with pytest.raises(InvalidNumberError):
        round_decimal(text, 2)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_floats(value: float) -> None:
    with pytest.raises(InvalidNumberError):
        format_sig(value, 2)


@pytest.mark.parametrize("figures", [0, -1])
def test_invalid_figures(figures: int) -> None:
    with pytest.raises(InvalidFiguresError):
        round_sig(1, figures)


def test_unknown_rounding() -> None:
    with pytest.raises(InvalidOptionError, match="half_even"):
        round_decimal(1, 2, rounding="nearest")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("value", "figures"), [(True, 2), (None, 2), ([1], 2), (1, 2.0), (1, True)]
)
def test_wrong_types_raise_type_error(value: object, figures: object) -> None:
    with pytest.raises(TypeError):
        round_decimal(value, figures)  # type: ignore[arg-type]


def test_0_1_0_callers_catching_value_error_still_work() -> None:
    for call in (lambda: round_sig("x", 2), lambda: format_sig(1, 0)):
        with pytest.raises(ValueError):
            call()


def test_errors_are_exported() -> None:
    for error in ERRORS:
        assert getattr(sigfigs, error.__name__) is error
