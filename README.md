# sigfigs

Significant-figures rounding and formatting with exact Decimal math and preserved trailing zeros

## Install

```
pip install sigfigs
```

## Usage

```python
from sigfigs import round_sig, format_sig

round_sig(123456, 3)        # 123000.0
round_sig(0.00123456, 3)    # 0.00123
round_sig(2.675, 3)         # 2.68, exact: no binary float drift
round_sig(-0.0987, 2)       # -0.099

format_sig(1.2, 3)          # "1.20", trailing zeros kept
format_sig(1, 3)            # "1.00"
format_sig(1234, 2)         # "1200"
format_sig(0, 3)            # "0.00"
format_sig(0.00012345, 2, sci=True)  # "1.2e-04"
```

`round_sig(x, figures)` returns a `float` rounded to the requested number of
significant figures. `format_sig(x, figures)` returns a string with exactly that
many significant figures, keeping the trailing zeros a `float` would drop, and
switches to scientific notation with `sci=True`.

Both accept an `int`, `float`, `str` or `Decimal`. Values are converted through
`decimal.Decimal` so the rounding matches the decimal digits you see rather than
the binary approximation (`round_sig(2.675, 3)` is `2.68`, not `2.67`). Rounding
is half to even. Non-finite values and figures below one are rejected.

## Why

The standard library rounds to decimal places, not to significant figures, and
`round` operates on binary floats, so `round(2.675, 2)` gives `2.67`. Formatting
to a fixed number of significant figures while keeping trailing zeros, across
zero, negatives and very large or small magnitudes, takes fiddly string work
every time.

The one option with real traction, `sigfig`, is a single module of several
hundred lines covering uncertainty, ranges and more, and it ships no `py.typed`.
`sigfigs` is the small, dependency-free, fully typed take: two functions, exact
Decimal math, `mypy --strict` clean.

## License

MIT. See [LICENSE](LICENSE).

## Links

- Website: https://lianes8studio.com
- GitHub: https://github.com/JaviLianes8
- LinkedIn: https://www.linkedin.com/in/jlianes/
