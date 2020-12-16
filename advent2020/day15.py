from __future__ import annotations

from typing import List, Iterator, Dict
import itertools

def play_game(starting_numbers: List[int]) -> Iterator[int]:
    last_seen: Dict[int, int] = {}
    gap = None

    for i in itertools.count(0):
        if i < len(starting_numbers):
            # still in starting numbers, use them
            n = starting_numbers[i]
        elif gap:
            # number seen before, so say the gap
            n = gap 
        else:
            # new number, so say zero
            n = 0
        
        if n in last_seen:
            # saw this already, so figure out the gap
            gap = i - last_seen[n]
        else:
            # first time, so no gap
            gap = None

        # update last seen and yield
        last_seen[n] = i
        yield n

def n2020(starting_numbers: List[int]) -> int:
    game = play_game(starting_numbers)
    for i in range(2020):
        n = next(game)
    return n

def n30000000(starting_numbers: List[int]) -> int:
    game = play_game(starting_numbers)
    for i in range(30000000):
        if i % 1000 == 0:
            print(i, i / 30000000)
        n = next(game)
    return n


#
# unit tests
#

game = play_game([0, 3, 6])
output = [next(game) for _ in range(10)]
assert n2020([0, 3, 6]) == 436

# 
# problem
#

numbers = [2,20,0,4,1,17]
# print(n2020(numbers))
# print(n30000000(numbers))