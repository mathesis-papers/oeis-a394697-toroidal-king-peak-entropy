# Toroidal king peak entropy

The note proves the all-integer limit in Kotěšovec's conjecture, added to OEIS A394697 in history revision 21 on 6 May 2026 and retained in entry revision 24: the largest independence-polynomial coefficient on an n-by-n toroidal king board has n²th root tending to A247413. Extending Liang (2025), it proves fixed-positive-activity limits on arbitrary growing rectangles, explicit entropy error bounds, marked-count moment limits, even-size maximum-packing counts and density, and infinitely many scalar log-concavity failures.

## Files

- `note.tex`: the self-contained mathematical argument and checked bibliography.
- `note.pdf`: the typeset note.
- `metadata.json`: authors, license, problem identifiers, and mathematical coverage.
- `verify.py`: exact integer coefficient enumeration and rational-activity comparisons.
- `checks.json`: the expected deterministic output of `verify.py`.
- `sibling_checks.py`: rectangular comparisons, marked moments, and exact inequalities on the listed OEIS values.
- `sibling-checks.json`: the expected deterministic output of `sibling_checks.py`.

## Build

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively, use a LaTeX distribution with `pdflatex`, `geometry`, `lmodern`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `url`, and `hyperref`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is embedded in `note.tex`; a separate BibTeX step is unnecessary.

## Finite calculations

Python 3.10 or newer, using the standard library only:

```sh
python3 verify.py > computed.json
cmp computed.json checks.json
python3 sibling_checks.py > computed-siblings.json
cmp computed-siblings.json sibling-checks.json
```

The first checker enumerates complete toroidal independence polynomials for 3 ≤ n ≤ 8 and free/cylindrical counterparts. A vertex include/exclude recurrence independently agrees with the row-state enumeration at n = 3, 4 for all three boundary conditions. The second checker covers widths 3,...,6 and heights 3,...,8, comparing both enumeration methods on 3x3, 3x4, and 4x3 boards. Seam, maximum-versus-sum and moment bounds use exact activities 1/2, 1, 2; moment powers are 0, 1, 2, 3. Comparisons of the A394697 b-file values establish scalar log-concavity failures at all indices 4,...,20 and increasing normalized peak entropy for the listed sizes 3,...,21; independent coefficient enumeration covers 3,...,8. These are finite calculations; the infinite limits have written proofs in Theorem 1 and Corollaries 3–5.

## Mathematical sources and coverage

The posing source is [OEIS A394697, revision 24](https://github.com/oeis/oeisdata/blob/77073cc8105b8042be07ec0d885da5ea5960ff3c/seq/A394/A394697.seq). The [entry history](https://oeis.org/history?seq=A394697) identifies the conjecture's original posting as history revision 21, 6 May 2026. Václav Kotěšovec posed the conjecture; Todd Hildebrant authored the entry. The same OEIS data revision fixes A247413, A063443, A067958, A212269, and A189889. The coverage table separates prior results, proved extensions and finite observations. Universal normalized-entropy monotonicity, the exact odd-size A189889 formula and surface-coefficient convergence remain outside its scope.

The all-integer epsilon–N statement is `D5.S3.Combinatorics.Graph.Pressure.ToroidalKingsPeakEntropy.result` in the [pinned Lean file](https://github.com/the-omega-institute/trureturing/blob/074df09ddbbef1843ddb383577bfaa827f753e36/D5/S3/Combinatorics/Graph/Pressure/ToroidalKingsPeakEntropy.lean). Its constant is defined from the square-tiling count. The [seam declarations](https://github.com/the-omega-institute/trureturing/blob/074df09ddbbef1843ddb383577bfaa827f753e36/D5/S3/Combinatorics/Graph/Pressure/ToroidalKingsEmptySeam.lean) give the free/toroidal inequalities, coefficient bound, tiling identity and free-entropy limit. [RectangularCountEntropy.square_log_limit](https://github.com/the-omega-institute/trureturing/blob/074df09ddbbef1843ddb383577bfaa827f753e36/D5/S3/Combinatorics/Graph/Pressure/RectangularCountEntropy.lean) gives a square limit for symmetric separately subadditive rectangular log-counts with a linear area bound. The weighted rectangular and marked-count extensions, packing consequences and infinitely-many-failures statement have written proofs in the note; they are distinct from these formal counterparts.

## Authors and license

1. Haobo Ma — ChronoAI Pte Ltd, Singapore.
2. Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Copyright 2026 Haobo Ma and Wenlin Zhang. [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) (`cc-by-4.0`).
