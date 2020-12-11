from __future__ import annotations
from typing import List
from collections import Counter

Grid = List[List[str]]

neighbors = [(-1, 0), (-1, -1), (-1, +1), 
             ( 0,-1),           ( 0, +1),
             ( 1, 1), (1,  0),  (1, - 1)]

def next_value(grid: Grid, i: int, j: int) -> str:
    nr = len(grid)
    nc = len(grid[0])

    counts = Counter(
        grid[i + di][j + dj]
        for di, dj in neighbors
        if 0 <= i + di < nr and 0 <= j + dj < nc
    )

    c = grid[i][j]    

    if c == 'L' and counts['#'] == 0:
        return '#'
    if c == '#' and counts['#'] >= 4:
        return 'L'
    else:
        return c

def step(grid: Grid) -> Grid:
    return [
        [
            next_value(grid, i, j)
            for j, c in enumerate(row)
        ]
        for i, row in enumerate(grid)
    ]

def final_seats(grid: Grid) -> int:
    while True:
        next_grid = step(grid)
        if next_grid == grid:
            break
        grid = next_grid

    return sum(c == '#' for row in grid for c in row)


### PART 2


def first_seat(grid: Grid, i: int, j: int, di: int, dj: int) -> str:
    nr = len(grid)
    nc = len(grid[0])

    while True:
        i += di
        j += dj

        if 0 <= i < nr and 0 <= j < nc:
            c = grid[i][j]
            if c == '#' or c == 'L':
                return c
        else:
            return '.'


def next_value2(grid: Grid, i: int, j: int) -> str:
    counts = Counter(
        first_seat(grid, i, j, di, dj)
        for di, dj in neighbors
    )

    c = grid[i][j]    

    if c == 'L' and counts['#'] == 0:
        return '#'
    if c == '#' and counts['#'] >= 5:
        return 'L'
    else:
        return c


def step2(grid: Grid) -> Grid:
    return [
        [
            next_value2(grid, i, j)
            for j, c in enumerate(row)
        ]
        for i, row in enumerate(grid)
    ]

def final_seats2(grid: Grid) -> int:
    while True:
        next_grid = step2(grid)
        if next_grid == grid:
            break
        grid = next_grid

    return sum(c == '#' for row in grid for c in row)


#
# unit tests
#

RAW = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

GRID = [list(row) for row in RAW.split("\n")]

assert final_seats(GRID) == 37
assert final_seats2(GRID) == 26

#
# problem
#
with open('inputs/day11.txt') as f:
    grid = [list(line.strip()) for line in f]

# print(final_seats(grid))
print(final_seats2(grid))