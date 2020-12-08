"""
BFFFBBFRRR: row 70, column 7, seat ID 567.
FFFBBBFRRR: row 14, column 7, seat ID 119.
BBFFBBFRLL: row 102, column 4, seat ID 820.
"""

from typing import NamedTuple

class Seat(NamedTuple):
    row: int
    col: int

    @property
    def seat_id(self) -> int:
        return self.row * 8 + self.col

def find_seat(bp: str) -> Seat:
    row = 0
    col = 0

    for i, c in enumerate(bp[:7]):
        multiplier = 2 ** (6 - i)
        include = 1 if c == 'B' else 0
        row += multiplier * include

    for i, c in enumerate(bp[-3:]):
        multiplier = 2 ** (2 - i)
        include = 1 if c == 'R' else 0
        col += multiplier * include

    return Seat(row, col)

def find_seat2(bp: str) -> Seat:
    row = int(''.join({'B': '1', 'F': '0'}[c] for c in bp[:7]), 2)
    col = int(''.join({'R': '1', 'L': '0'}[c] for c in bp[-3:]), 2)
    return Seat(row, col)

#
# PROBLEMS
#

with open('inputs/day05.txt') as f:
    seats = [find_seat2(bp.strip()) for bp in f]

print(max(seat.seat_id for seat in seats))

seat_ids = [seat.seat_id for seat in seats]

lo = min(seat_ids)
hi = max(seat_ids)

print([x for x in range(lo, hi) 
        if x not in seat_ids]) # and x-1 in seat_ids and x+1 in seat_ids])