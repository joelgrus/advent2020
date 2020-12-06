from typing import List
from collections import Counter

RAW = """abc

a
b
c

ab
ac

a
a
a
a

b"""

def count_yeses(raw: str) -> int:
    groups = raw.split("\n\n")
    num_yeses = 0
    for group in groups:
        people = group.split("\n")
        yeses = {c for person in people for c in person}
        num_yeses += len(yeses)
    return num_yeses

assert count_yeses(RAW) == 11

def count_yeses2(raw: str) -> int:
    groups = raw.split("\n\n")
    num_yeses = 0
    for group in groups:
        people = group.split("\n")
        yeses = Counter(c for person in people for c in person)
        num_yeses += sum(count == len(people) for c, count in yeses.items())
    return num_yeses

assert count_yeses2(RAW) == 6


with open('inputs/day06.txt') as f:
    raw = f.read()
    print(count_yeses(raw))
    print(count_yeses2(raw))