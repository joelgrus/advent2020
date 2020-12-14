from __future__ import annotations

from typing import List
from functools import reduce

def earliest_bus(depart: int, buses: List[int]) -> int:
    missed_by = [depart % bus for bus in buses]
    waits = {
        bus: bus - miss if miss > 0 else 0 
        for bus, miss in zip(buses, missed_by)
    }

    # choose the bus with the lowest wait
    bus = min(buses, key=lambda bus: waits[bus])

    return bus * waits[bus]


def make_factors(raw_buses: List[str]):
    indexed = [(i, int(bus)) for i, bus in enumerate(raw_buses) if bus != 'x']
    factors = [(bus, (bus - i) % bus) for i, bus in indexed]
    return factors

# chinese remainder code from
# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


# Thanks to YouTube commenter Paul Fornia who suggested this approach.
def chinese_remainder2(divisors: List[int], remainders: List[int]) -> int:
    solution = remainders[0]
    increment = divisors[0]

    # invariant: at step i, we have that 
    #     `solution % d[j] == r[j]` 
    #     `increment % d[j] == 0`
    # for all i <= j. In particular, we can add multiples of `increment`
    # to `solution` without changing the first invariant.

    for d, r in zip(divisors[1:], remainders[1:]):
        while solution % d != r:
            solution += increment
        increment *= d 

    return solution % increment

#
# unit tests
#

RAW = """939
7,13,x,x,59,x,31,19"""

L1, L2 = RAW.split("\n")
DEPART = int(L1)
BUSES = [int(x) for x in L2.split(",") if x != "x"]
assert earliest_bus(DEPART, BUSES) == 295

#
# scratch around
#

"""
7,13,x,x,59,x,31,19

find t such that

t % 7 == 0
t % 13 == 13 - 1
skip 2
skip 3
t % 59 == 59 - 4
skip 5
t % 31 == 31 - 6
t % 19 == 19 - 7
"""

#
# problem
#

with open('inputs/day13.txt') as f:
    depart = int(next(f))
    buses_raw = [x for x in next(f).split(",")]
    buses = [int(x) for x in buses_raw if x != "x"]


print(earliest_bus(depart, buses))

n, a = zip(*make_factors(buses_raw))

