from __future__ import annotations
from collections import deque
import itertools

class CupGame:
    def __init__(self, cups: str) -> None:
        self.cups = deque([int(c) for c in cups])
        self.lo = min(self.cups)
        self.hi = max(self.cups)

    def move(self) -> None:
        # Get the current cup and move it to the end
        current = self.cups.popleft()
        self.cups.append(current)

        # take the next 3
        c1 = self.cups.popleft()
        c2 = self.cups.popleft()
        c3 = self.cups.popleft()        

        missing = [c1, c2, c3]

        destination = current - 1
        while not destination in self.cups:
            destination -= 1
            if destination < self.lo:
                destination = self.hi
        
        # now rotate to get to destination
        while True:
            cup = self.cups.popleft()
            self.cups.append(cup)
            if cup == destination:
                break

        self.cups.extend(missing)

        # now rotate to the cup after current
        while True:
            cup = self.cups.popleft()
            self.cups.append(cup)
            if cup == current:
                break

    def labels(self) -> str:
        while True:
            cup = self.cups.popleft()
            self.cups.append(cup)
            if cup == 1:
                return ''.join(str(i) for i in list(self.cups)[:-1])


from dataclasses import dataclass

@dataclass
class Node:
    """
    We need a linked list to represent the cycle
    """
    value: int
    prev: Node
    next: Node

class CupGame2:
    def __init__(self, raw_cups: str) -> None:        
        cups = [int(c) for c in raw_cups]
        self.current = prev = cups[0]
        self.nodes = {prev: Node(prev, None, None)}
        for cup in itertools.chain(cups[1:], range(max(cups) + 1, 1_000_001)):
            # add backlink to previous node
            self.nodes[cup] = Node(cup, self.nodes[prev], None)
            # add forward link from previous node
            self.nodes[prev].next = self.nodes[cup]
            prev = cup 
        # add links between end and beginning
        self.nodes[self.current].prev = self.nodes[cup]
        self.nodes[cup].next = self.nodes[self.current]

        assert len(self.nodes) == 1_000_000 

    def ten_from(self, n: int):
        """just for debugging"""
        node = self.nodes[n]
        for _ in range(10):
            print(node.value, end=',')
            node = node.next

    def move(self) -> None:
        current = self.nodes[self.current]

        # find next 3 nodes
        n1 = current.next
        n2 = n1.next
        n3 = n2.next
        rest = n3.next

        # get their values        
        v1 = n1.value
        v2 = n2.value
        v3 = n3.value

        # remove them
        current.next = rest 
        rest.prev = current

        # null out their pointers so they can be garbage collected
        n1.next = n1.prev = n2.next = n2.prev = n3.next = n3.prev = None

        def decrement(dest: int) -> int:
            if dest <= 1:
                return 1_000_000
            else:
                return dest - 1

        destination = decrement(current.value)
        while destination in [v1, v2, v3]:
            destination = decrement(destination)
        
        # insert the missing nodes
        dest_node = self.nodes[destination]
        rest = dest_node.next
        n1_new = Node(v1, dest_node, None)
        n2_new = Node(v2, n1_new, None)
        n3_new = Node(v3, n2_new, rest)

        self.nodes[v1] = n1_new
        self.nodes[v2] = n2_new
        self.nodes[v3] = n3_new

        dest_node.next = n1_new
        n1_new.next = n2_new
        n2_new.next = n3_new
        rest.prev = n3_new
        
        self.current = self.nodes[self.current].next.value


#
# unit tests
#

RAW = "389125467"
GAME = CupGame(RAW)
for i in range(100):
    GAME.move()
    print(i, GAME.cups)
assert GAME.labels() == "67384529"

GAME2 = CupGame2(RAW)
# for i in range(1_000_000):
#     seen = set()
#     curr = GAME2.nodes[GAME2.current]
#     for _ in range(1_000_000):
#         seen.add(curr.value)
#         curr = curr.next
#     print(i, len(seen))
#     if len(seen) < 1_000_000:
#         break
#     GAME2.move()

# for i in range(10_000_000):
#     # if i % 1000 == 0:
#     #     print(i)
#     GAME2.move()
# node = GAME2.nodes[1]
# print(node.next.value, node.next.next.value)


# 
# problem
#

# with open('inputs/day23.txt') as f:
#     raw = f.read()

raw = "157623984"
# game = CupGame(raw)
# for _ in range(100):
#     game.move()
# print(game.labels())
game2 = CupGame2(raw)
for i in range(10_000_000):
    if i % 1000 == 0:
        print(i)
    game2.move()
node = game2.nodes[1]
print(node.next.value * node.next.next.value)