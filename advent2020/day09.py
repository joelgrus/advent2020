from __future__ import annotations

from typing import List, Iterator
from collections import deque


def not_sums(numbers: List[int], lookback: int = 25) -> Iterator[int]:
    q = deque()
    for n in numbers:
        if len(q) < lookback:
            q.append(n)
        else:
            sums = {a + b 
                    for i, a in enumerate(q)
                    for j, b in enumerate(q)
                    if i < j}
            if n not in sums:
                yield n
            q.append(n)
            q.popleft()

def range_with_sum(numbers: List[int], target: int) -> List[int]:
    for i, n in enumerate(numbers):
        j = i
        total = n
        while total < target and j < len(numbers):
            j += 1
            total += numbers[j]
        if total == target and i < j:
            slice = numbers[i:j+1]
            return slice

    raise RuntimeError()


def encryption_weakness(numbers: List[int], lookback: int = 25) -> int:
    target = next(not_sums(numbers, lookback))
    slice = range_with_sum(numbers, target)
    return min(slice) + max(slice)

#
# Unit Tests
#

RAW = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

NUMBERS = [int(x) for x in RAW.split("\n")]

assert next(not_sums(NUMBERS, 5)) == 127

assert encryption_weakness(NUMBERS, 5) == 62

# 
# Problem
#

with open('inputs/day09.txt') as f:
    raw = f.read()

numbers = [int(x) for x in raw.split("\n")]
print(next(not_sums(numbers)))
print(encryption_weakness(numbers))