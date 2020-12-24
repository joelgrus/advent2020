from __future__ import annotations
from typing import List, Tuple, Set, Dict, Iterator
from collections import Counter

Hex = Tuple[float, float]

def parse(raw: str) -> List[str]:
    """
    directions are e, ne, se, w, nw, sw

          nw  ne
        w - o -  e
          se  sw
    """
    out = []
    while raw:
        if raw[:2] in ("nw", "ne", "sw", "se"):
            out.append(raw[:2])
            raw = raw[2:]
        else:
            out.append(raw[0])
            raw = raw[1:]
    return out

def find_tile(steps: List[str]) -> Hex:
    """returns final (x, y)"""
    x = y = 0
    for step in steps:
        if step == "e":
            x += 1
        elif step == "ne":
            x += 0.5
            y += 1
        elif step == "nw":
            x -= 0.5
            y += 1
        elif step == "w":
            x -= 1
        elif step == "sw":
            x -= 0.5
            y -= 1
        elif step == "se":
            x += 0.5
            y -= 1

    return x, y 

def find_black_tiles(raw: str) -> Set[Hex]:
    counts: Dict[Hex, int] = Counter()

    for line in raw.split("\n"):
        steps = parse(line)
        x, y = find_tile(steps)
        counts[(x, y)] += 1

    return {k for k, v in counts.items() if v % 2 == 1}


def count_black_tiles(raw: str) -> int:
    return len(find_black_tiles(raw))

def neighbors(hex: Hex) -> Iterator[Hex]:
    x, y = hex
    yield x + 1, y         # e
    yield x - 1, y         # w
    yield x + 0.5, y + 1   # ne
    yield x - 0.5, y + 1   # nw
    yield x + 0.5, y - 1   # se
    yield x - 0.5, y - 1   # sw

def step(black_tiles: Set[Hex]) -> Set[Hex]:
    neighbor_counts = Counter()
    for hex in black_tiles:
        for neighbor in neighbors(hex):
            neighbor_counts[neighbor] += 1
    
    return {
        hex 
        for hex, count in neighbor_counts.items()
        if (hex in black_tiles and 1 <= count <= 2) or (hex not in black_tiles and count == 2)
    }

#
# unit testing
#

RAW = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

assert count_black_tiles(RAW) == 10

# 
# problem
#

with open('inputs/day24.txt') as f:
    raw = f.read()

print(count_black_tiles(raw))

tiles = find_black_tiles(raw)
for _ in range(100):
    tiles = step(tiles)
print(len(tiles))