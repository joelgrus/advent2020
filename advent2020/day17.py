from __future__ import annotations
from typing import NamedTuple, Set, Iterator, Tuple, List
import itertools


Point = Tuple[int, ...]


def neighbors(point: Point) -> Iterator[Point]:
    dim = len(point)
    changes = [[-1, 0, 1] for _ in range(dim)]
    for deltas in itertools.product(*changes):
        if any(d != 0 for d in deltas):
            p: List[int] = [x + dx for x, dx in zip(point, deltas)]
            yield tuple(p)

Grid = Set[Point]


def step(grid: Grid) -> Grid:
    new_candidates = {
        p 
        for point in grid 
        for p in neighbors(point)
        if p not in grid
    }

    new_grid = set()

    for point in grid:
        n = sum(p in grid for p in neighbors(point))
        if n in (2, 3):
            new_grid.add(point)

    for point in new_candidates:
        n = sum(p in grid for p in neighbors(point))
        if n == 3:
            new_grid.add(point)

    return new_grid

def make_grid(raw: str, dim: int):
    lines = raw.split("\n")
    pad = tuple([0] * (dim-2))
    return {
        (x, y) + pad
        for y, row in enumerate(lines)
        for x, c in enumerate(row)
        if c == '#'
    }

#
# unit tests
#

RAW = """.#.
..#
###"""

GRID3 = make_grid(RAW, 3)

for _ in range(6):
    GRID3 = step(GRID3)

assert len(GRID3) == 112

GRID4 = make_grid(RAW, 4)

for _ in range(6):
    GRID4 = step(GRID4)

assert len(GRID4) == 848

# 
# problem
#

with open('inputs/day17.txt') as f:
    raw = f.read()

grid3 = make_grid(raw, 3)
for _ in range(6):
    grid3 = step(grid3)
print(len(grid3))

grid4 = make_grid(raw, 4)
for i in range(6):
    print(i)
    grid4 = step(grid4)
print(len(grid4))
