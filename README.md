# sigfigs

Significant-figures rounding and formatting with exact Decimal math and preserved trailing zeros

## Install

```
pip install sigfigs
```

## Usage

```python
from sigfigs import (
    count_sig, format_sig, format_uncertainty, round_decimal, round_sig, sig_bounds,
)

round_sig(123456, 3)        # 123000.0
round_sig(2.675, 3)         # 2.68, exact: no binary float drift
round_decimal(1.2, 3)       # Decimal('1.20'), the exponent records the figures
round_decimal("2.5", 1, rounding="half_up")  # Decimal('3'), eight rounding modes

format_sig(1.2, 3)          # "1.20", trailing zeros kept
format_sig(0, 3)            # "0.00"
format_sig(0.00012345, 2, sci=True)          # "1.2e-04"
format_sig(123456, 4, notation="eng")        # "123.5e+03"
format_sig(1000, 4, trailing_point=True)     # "1000."

count_sig("0.00120")        # 3
count_sig("6.022e23")       # 4
sig_bounds("1200")          # (2, 4), trailing zeros without a point are ambiguous

format_uncertainty(100.02147, 0.00035)               # "100.02147(35)"
format_uncertainty(100.02147, 0.00035, style="pm")   # "100.02147 +/- 0.00035"
```

All functions accept an `int`, `float`, `str` or `Decimal`. Values are converted
through `decimal.Decimal` so the rounding matches the decimal digits you see rather
than the binary approximation: a float is read through `repr`, so
`round_sig(2.675, 3)` is `2.68`, not `2.67`. Rounding is half to even by default
(NIST SP 811 B.7.1, the IEEE 754 default) and every `decimal` rounding mode is
available. Values with an uncertainty follow the GUM (JCGM 100:2008, clause 7.2):
the uncertainty keeps two significant figures and the value is rounded to match.

Errors are typed (`InvalidNumberError`, `InvalidFiguresError`, `InvalidOptionError`,
`AmbiguousFiguresError`, `UncertaintyError`), all subclasses of `SigFigsError` and
of `ValueError`.

## Command line

```
sigfigs round 2.675 3                    # 2.68
sigfigs round 123456 2 --notation sci    # 1.2e+05
sigfigs count 0.00120 1200 1200.         # 3, 2, 4
sigfigs format 100.02147 -u 0.00035      # 100.02147(35)
```

See [GUIDE.md](GUIDE.md) for every rule, the command options, the cited sources and
how the results differ from `format(x, ".{n}g")`.

## Why

The standard library rounds to decimal places, not to significant figures, and
`round` operates on binary floats, so `round(2.675, 2)` gives `2.67`. Formatting
to a fixed number of significant figures while keeping trailing zeros, across
zero, negatives and very large or small magnitudes, takes fiddly string work
every time.

The one option with real traction, `sigfig`, is a single module of several
hundred lines covering uncertainty, ranges and more, and it ships no `py.typed`.
`sigfigs` is the small, dependency-free, fully typed take: exact Decimal math,
source-checked rules, `mypy --strict` clean.

## License

MIT. See [LICENSE](LICENSE).

## Links

- Website: https://lianes8studio.com
- GitHub: https://github.com/JaviLianes8
- LinkedIn: https://www.linkedin.com/in/jlianes/
