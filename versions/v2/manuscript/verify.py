#!/usr/bin/env python3
import json
from fractions import Fraction
from functools import cache


def row_states(width, periodic):
    return [
        mask for mask in range(1 << width)
        if not mask & (mask << 1)
        and not (periodic and mask & 1 and mask & (1 << (width - 1)))
    ]


def row_compatible(first, second, width, periodic):
    neighbors = second | (second << 1) | (second >> 1)
    if periodic:
        neighbors |= ((second & 1) << (width - 1)) | (second >> (width - 1))
    return not first & neighbors


def polynomial(side, boundary, height=None):
    if height is None:
        height = side
    if side == 0:
        return [1]
    horizontal_periodic = boundary != 'free'
    states = row_states(side, horizontal_periodic)
    neighbors = {
        first: [second for second in states
                if row_compatible(first, second, side, horizontal_periodic)]
        for first in states
    }
    weights = {state: state.bit_count() for state in states}
    result = [0] * (side * height + 1)
    starts = states if boundary == 'torus' else [None]
    for start in starts:
        dynamic = {}
        for state in states:
            if start is None or state == start:
                values = [0] * (weights[state] + 1)
                values[weights[state]] = 1
                dynamic[state] = values
        for unused_row in range(1, height):
            following = {}
            for first, values in dynamic.items():
                for second in neighbors[first]:
                    shift = weights[second]
                    target = following.setdefault(second, [])
                    if len(target) < len(values) + shift:
                        target.extend([0] * (len(values) + shift - len(target)))
                    for degree, count in enumerate(values):
                        target[degree + shift] += count
            dynamic = following
        for last, values in dynamic.items():
            if start is None or start in neighbors[last]:
                for degree, count in enumerate(values):
                    result[degree] += count
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def graph_polynomial(side, boundary, height=None):
    if height is None:
        height = side
    vertices = [(row, column) for row in range(height) for column in range(side)]
    adjacency = []
    for first_index, first in enumerate(vertices):
        mask = 0
        for second_index, second in enumerate(vertices):
            row_gap = abs(first[0] - second[0])
            column_gap = abs(first[1] - second[1])
            if boundary == 'torus':
                row_gap = min(row_gap, height - row_gap)
            if boundary != 'free':
                column_gap = min(column_gap, side - column_gap)
            if first_index != second_index and row_gap <= 1 and column_gap <= 1:
                mask |= 1 << second_index
        adjacency.append(mask)

    @cache
    def include_exclude(remaining):
        if not remaining:
            return (1,)
        selected_bit = remaining & -remaining
        selected_index = selected_bit.bit_length() - 1
        without = remaining ^ selected_bit
        excluded = include_exclude(without)
        included = include_exclude(without & ~adjacency[selected_index])
        values = [0] * max(len(excluded), len(included) + 1)
        for degree, count in enumerate(excluded):
            values[degree] += count
        for degree, count in enumerate(included):
            values[degree + 1] += count
        return tuple(values)

    return list(include_exclude((1 << len(vertices)) - 1))


def weighted_total(values, activity):
    return sum(count * activity ** degree for degree, count in enumerate(values))


def main():
    expected_peaks = {3: 9, 4: 56, 5: 600, 6: 14940, 7: 576856, 8: 42752576}
    expected_torus = {3: 10, 4: 133, 5: 1411, 6: 42938, 7: 1796859, 8: 157763829}
    expected_free = [1, 2, 5, 35, 314, 6427, 202841, 12727570, 1355115601]
    expected_cylinder = {3: 19, 4: 205, 5: 3011, 6: 92875, 7: 4763459, 8: 459630701}
    free = {side: polynomial(side, 'free') for side in range(9)}
    assert [sum(free[side]) for side in range(9)] == expected_free
    rows = []
    for side in range(3, 9):
        torus = polynomial(side, 'torus')
        cylinder = polynomial(side, 'cylinder')
        assert max(torus) == expected_peaks[side]
        assert sum(torus) == expected_torus[side]
        assert sum(cylinder) == expected_cylinder[side]
        assert torus[0] == 1 and torus[1] == side * side
        if side <= 4:
            for boundary, values in [('torus', torus), ('cylinder', cylinder), ('free', free[side])]:
                assert graph_polynomial(side, boundary) == values
        for activity in [Fraction(1, 2), Fraction(1), Fraction(2)]:
            free_smaller = weighted_total(free[side - 1], activity)
            toroidal = weighted_total(torus, activity)
            cylindrical = weighted_total(cylinder, activity)
            free_same = weighted_total(free[side], activity)
            peak = max(count * activity ** degree for degree, count in enumerate(torus))
            assert free_smaller <= toroidal <= cylindrical <= free_same
            assert peak <= toroidal <= (side * side + 1) * peak
        rows.append({
            'n': side,
            'free_total': sum(free[side]),
            'cylinder_total': sum(cylinder),
            'torus_total': sum(torus),
            'torus_peak': max(torus),
            'modal_sizes': [degree for degree, count in enumerate(torus) if count == max(torus)],
            'torus_coefficients': torus,
        })
    assert expected_peaks[4] ** 2 == 3136 < 5400 == expected_peaks[3] * expected_peaks[5]
    result = {
        'schema_version': 1,
        'coverage': {
            'row_transfer_polynomials': 'Free, cylindrical, and toroidal squares with 3 <= n <= 8; free squares also with 0 <= n <= 2.',
            'independent_vertex_recurrence': 'All three boundary conditions with n in {3,4}; equality of complete coefficient lists.',
            'weighted_inequalities': 'Exact rational activities 1/2, 1, 2 with 3 <= n <= 8.',
            'infinite_limits': 'Written proofs in note.tex, Theorem 1 and Corollary 3.',
        },
        'rows': rows,
        'scalar_log_concavity_counterexample': {'n': 4, 'a_n_squared': 3136, 'a_previous_times_a_next': 5400},
        'all_checks_passed': True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
