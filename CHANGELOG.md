# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-10-13

### Changed

- The `rounding.decTest` excerpt is no longer committed or shipped in the sdist:
  `scripts/fetch_upstream.py` fetches the General Decimal Arithmetic test archive,
  checked against `tests/upstream/MANIFEST.json`, and a hand-written table covers every
  rounding mode when it is absent.

## [0.2.0]

- Add `rounding=` to `round_sig` and `format_sig` with eight modes (`half_even`
  default, `half_up`, `half_down`, `up`, `down`, `ceiling`, `floor`, `05up`).
- Add `round_decimal`, returning an exact `Decimal` whose exponent records the
  significant figures.
- Add `count_sig` and `sig_bounds` to count the significant figures of a written
  number, with ambiguous trailing zeros reported or rejected (`strict=True`).
- Add `notation=` (`fixed`, `sci`, `eng`) and `trailing_point=` to `format_sig`.
- Add `round_uncertainty` and `format_uncertainty` for values with a standard
  uncertainty, in the `1.234(5)` and `1.234 +/- 0.005` forms of JCGM 100:2008.
- Add typed errors under `SigFigsError`; all remain `ValueError` subclasses.
- Add the `sigfigs` command (`round`, `count`, `format`) and `python -m sigfigs`.
- Read floats through `repr` (unchanged results; `str` and `repr` agree for floats).
- Add `GUIDE.md`.

## [0.1.0]

- Add `round_sig` to round a number to a given count of significant figures.
- Add `format_sig` to format significant figures as a string, keeping trailing
  zeros, with optional scientific notation.
