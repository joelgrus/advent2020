from __future__ import annotations
from typing import List, Dict

from collections import Counter

def count_skips(adapters: List[int]) -> Counter:
    adapters = sorted(adapters + [0])
    adapters.append(max(adapters) + 3)

    diffs = [next_a - prev_a for prev_a, next_a in zip(adapters, adapters[1:])]
    assert all(1 <= diff <= 3 for diff in diffs)

    return Counter(diffs)

def count_paths(adapters: List[int]) -> int:
    adapters.append(0)
    adapters.append(max(adapters) + 3)

    output = adapters[-1]

    # num_ways[i] is the numbers of ways to get to i
    num_ways = [0] * (output + 1)

    num_ways[0] = 1

    if 1 in adapters:
        num_ways[1] = 1

    if 2 in adapters and 1 in adapters:
        num_ways[2] = 2
    elif 2 in adapters:
        num_ways[2] = 1

    for n in range(3, output + 1):
        if n not in adapters:
            continue

        num_ways[n] = num_ways[n-3] + num_ways[n-2] + num_ways[n-1]

    return num_ways[output]

#
# Unit Tests
#

RAW1 = """16
10
15
5
1
11
7
19
6
12
4"""

RAW2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

ADAPTERS1 = [int(x) for x in RAW1.split("\n")]
ADAPTERS2 = [int(x) for x in RAW2.split("\n")]

SKIPS1 = count_skips(ADAPTERS1)
assert SKIPS1[1] * SKIPS1[3] == 7 * 5

SKIPS2 = count_skips(ADAPTERS2)
assert SKIPS2[1] * SKIPS2[3] == 22 * 10

assert count_paths(ADAPTERS1) == 8
assert count_paths(ADAPTERS2) == 19208

#
# Problem
#

with open('inputs/day10.txt') as f:
    adapters = [int(x) for x in f]
    skips = count_skips(adapters)
    print(skips[1] * skips[3])
    print(count_paths(adapters))