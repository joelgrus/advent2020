from __future__ import annotations

from typing import List, NamedTuple, Tuple, Set

RAW = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

Point = Tuple[int, int]


class Slope(NamedTuple):
    trees: Set[Point]
    width: int
    height: int

    @staticmethod
    def parse(raw: str) -> Slope:
        lines = raw.split("\n")
        trees = {(x, y)
                 for y, row in enumerate(lines)
                 for x, c in enumerate(row.strip())
                 if c == '#'}
        width = len(lines[0])
        height = len(lines)

        return Slope(trees, width, height)

SLOPE = Slope.parse(RAW)

def count_trees(
    slope: Slope,
    right: int = 3,
    down: int = 1
) -> int:
    num_trees = 0
    x = 0
    for y in range(0, slope.height, down):
        if (x, y) in slope.trees:
            num_trees += 1
        x = (x + right) % slope.width 
    return num_trees

assert count_trees(SLOPE) == 7


with open('inputs/day03.txt') as f:
    raw = f.read()
slope = Slope.parse(raw)
print(count_trees(slope))

# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.

def trees_product(slope: Slope, slopes: List[Point]) -> int:
    product = 1
    for right, down in slopes:
        product *= count_trees(slope, right=right, down=down)

    return product

SLOPES = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

assert trees_product(SLOPE, SLOPES) == 336

print(trees_product(slope, SLOPES))