"""
I was so unhappy with how ugly my solution was
that I cleaned it up.
"""
from __future__ import annotations
import itertools
from typing import Optional, Iterable, List


class CupGame:
    def __init__(self, 
                 cups: Iterable[int], 
                 continue_to: Optional[int] = None) -> None:

        if continue_to:
            cups = itertools.chain(cups, range(max(cups) + 1, continue_to + 1))

        it = iter(cups)
        self.current = prev = next(it)
        self.nexts = {}

        for cup in it:
            self.nexts[prev] = prev = cup

        self.nexts[prev] = self.current
        self.max = max(self.nexts)

    def move(self) -> None:
        # find next 3 nodes
        n1 = self.nexts[self.current]
        n2 = self.nexts[n1]
        n3 = self.nexts[n2]
        rest = self.nexts[n3]

        # remove them
        self.nexts[self.current] = rest 

        destination = self.current
        while destination in [self.current, n1, n2, n3]:
            destination = self.max if destination == 1 else destination - 1
        
        # insert the missing nodes after destination
        self.nexts[destination], self.nexts[n3] = n1, self.nexts[destination]

        # update current
        self.current = self.nexts[self.current]

    def labels(self) -> str:
        out = []
        n = 1
        while self.nexts[n] != 1:
            n = self.nexts[n]
            out.append(str(n))
        
        return ''.join(out)

def parse(raw: str) -> List[int]:
    return [int(c) for c in list(raw)]

#
# unit tests
#

RAW = "389125467"
CUPS = parse(RAW)

GAME = CupGame(CUPS)
for i in range(100):
    GAME.move()
assert GAME.labels() == "67384529"

GAME2 = CupGame(CUPS, continue_to=1_000_000)
for i in range(10_000_000):
    GAME2.move()
n1 = GAME2.nexts[1]
n2 = GAME2.nexts[n1]
assert (n1, n2) == (934001, 159792)


# 
# problem
#

raw = "157623984"
cups = parse(raw)

game = CupGame(cups)
for _ in range(100):
    game.move()
print(game.labels())

game2 = CupGame(cups, continue_to=1_000_000)
for i in range(10_000_000):
    game2.move()
n1 = game2.nexts[1]
n2 = game2.nexts[n1]

print(n1 * n2)
