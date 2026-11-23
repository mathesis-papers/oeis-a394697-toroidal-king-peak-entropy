#!/usr/bin/env python3
import json
from fractions import Fraction

from verify import graph_polynomial, polynomial, weighted_total


def main():
    rows = []
    for width in range(3, 7):
        for height in range(3, 9):
            area = width * height
            polynomials = {boundary: polynomial(width, boundary, height)
                           for boundary in ['free', 'cylinder', 'torus']}
            smaller = polynomial(width - 1, 'free', height - 1)
            if (width, height) in [(3, 3), (3, 4), (4, 3)]:
                for boundary, values in polynomials.items():
                    assert values == graph_polynomial(width, boundary, height)
            for activity in [Fraction(1, 2), Fraction(1), Fraction(2)]:
                totals = {boundary: weighted_total(values, activity)
                          for boundary, values in polynomials.items()}
                assert weighted_total(smaller, activity) <= totals['torus']
                assert totals['torus'] <= totals['cylinder'] <= totals['free']
                assert totals['free'] <= (1 + activity) ** (width + height - 1) * weighted_total(smaller, activity)
                for boundary, values in polynomials.items():
                    peak = max(value * activity ** degree for degree, value in enumerate(values))
                    assert peak <= totals[boundary] <= (area + 1) * peak
                    for power in [0, 1, 2, 3]:
                        moment = sum(degree ** power * value * activity ** degree
                                     for degree, value in enumerate(values) if degree > 0)
                        assert totals[boundary] - 1 <= moment <= area ** power * totals[boundary]
            if width == height:
                degree = len(polynomials['torus']) - 1
                assert (width // 2) ** 2 <= degree <= area // 4
                if width % 2 == 0:
                    assert degree == area // 4
            rows.append({'width': width, 'height': height,
                         'totals_at_one': {boundary: sum(values) for boundary, values in polynomials.items()},
                         'toroidal_degree': len(polynomials['torus']) - 1})
    source_peaks = [
        9, 56, 600, 14940, 576856, 42752576, 5666291496, 1377165318000,
        602917863487951, 491349880347810732, 717837429519886358358,
        1906549046833287409861952, 9139679913945121323495407100,
        79450391756097313369708715135488, 1239633081570241324597609845836883982,
        35261313543116561639195408117355324062850,
        1810386347051588570707649810830064105133831508,
        169527082712490664927086120912037553936464485002480,
        28360431875794954750033862974873355178567089274257689896,
    ]
    peaks = dict(zip(range(3, 22), source_peaks))
    for side in range(3, 9):
        assert peaks[side] == max(polynomial(side, 'torus'))
    failures = [side for side in range(4, 21)
                if peaks[side] ** 2 < peaks[side - 1] * peaks[side + 1]]
    increasing = [side for side in range(3, 21)
                  if peaks[side + 1] ** (side * side) > peaks[side] ** ((side + 1) ** 2)]
    assert failures == list(range(4, 21))
    assert increasing == list(range(3, 21))
    print(json.dumps({
        'schema_version': 1,
        'coverage': {
            'rectangular_polynomials': '3 <= width <= 6; 3 <= height <= 8; free, cylindrical and toroidal boundaries.',
            'independent_vertex_recurrence': 'Complete coefficient lists on 3x3, 3x4 and 4x3 boards for all three boundaries.',
            'activity': ['1/2', '1', '2'],
            'moments': 'Integer powers 0, 1, 2, 3; the real-power limit has its written proof in Corollary 5.',
            'source_values': 'OEIS A394697 b-file, n = 3,...,21; independent enumeration for n = 3,...,8.',
        },
        'rows': rows,
        'source_values_url': 'https://oeis.org/A394697/b394697.txt',
        'source_values': {str(side): value for side, value in peaks.items()},
        'scalar_log_concavity_failure_indices': failures,
        'normalized_peak_entropy_increase_indices': increasing,
        'all_checks_passed': True,
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
