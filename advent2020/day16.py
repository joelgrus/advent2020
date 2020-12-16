from __future__ import annotations
from typing import Dict, List, NamedTuple, Tuple
import math

Range = Tuple[int, int]

def make_range(s: str) -> Range:
    lo, hi = s.split("-")
    return (int(lo), int(hi))

class Rule(NamedTuple):
    name: str
    ranges: Tuple[Range, Range]

    def is_valid(self, i: int) -> bool:
        return any(lo <= i <= hi for lo, hi in self.ranges)

    @staticmethod
    def parse(line: str) -> Rule:
        name, ranges = line.split(": ")
        r1, r2 = ranges.split(" or ")
        return Rule(
            name=name,
            ranges=(make_range(r1), make_range(r2))
        )

Ticket = List[int]

def make_ticket(s: str) -> Ticket:
    return [int(n) for n in s.split(",")]

class Problem(NamedTuple):
    rules: List[Rule]
    your_ticket: Ticket
    nearby_tickets: List[Ticket]

    def valid_for_any_field(self, i: int) -> bool:
        return any(rule.is_valid(i) for rule in self.rules)

    def is_invalid(self, ticket: Ticket) -> bool:
        for n in ticket:
            if not self.valid_for_any_field(n):
                return True
        return False

    def error_rate(self) -> int:
        return sum(
            n
            for ticket in self.nearby_tickets
            for n in ticket
            if not self.valid_for_any_field(n)
        )    

    def discard_invalid_tickets(self) -> Problem:
        valid_tickets = [
            t for t in self.nearby_tickets 
            if not self.is_invalid(t)
        ]
        return self._replace(nearby_tickets=valid_tickets)

    @staticmethod
    def parse(raw: str) -> Problem:
        a, b, c = raw.split("\n\n")
        b = b.split("\n")[-1]

        rules = [Rule.parse(line) for line in a.split("\n")]
        my_ticket = make_ticket(b)
        nearby_tickets = [make_ticket(line) for line in c.split("\n")[1:]]

        return Problem(rules, my_ticket, nearby_tickets)


def identify_fields(problem: Problem) -> List[str]:
    num_fields = len(problem.your_ticket)
    tickets = [problem.your_ticket] + problem.nearby_tickets

    # candidates[i] is the possibilities for the ith field
    candidates = [
        {rule for rule in problem.rules 
         if all(rule.is_valid(ticket[i]) for ticket in tickets)}
        for i in range(num_fields)
    ]

    while True:
        unique_rules = [rule for cand in candidates if len(cand) == 1 for rule in cand]
        if len(unique_rules) == num_fields:
            return [rule.name for cand in candidates for rule in cand]
        
        for i in range(num_fields):
            cand = candidates[i]
            if len(cand) > 1:
                cand = {rule for rule in cand if rule not in unique_rules}
                candidates[i] = cand


#
# unit test
#

RAW = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

PROBLEM = Problem.parse(RAW)

assert PROBLEM.error_rate() == 71

PROBLEM2 = PROBLEM.discard_invalid_tickets()

assert PROBLEM2.nearby_tickets == [[7, 3, 47]]

#
# problem
#

with open('inputs/day16.txt') as f:
    raw = f.read()
    problem = Problem.parse(raw)
    print(problem.error_rate())

    problem2 = problem.discard_invalid_tickets()
    fields = identify_fields(problem2)

    departure_values = [
        n 
        for name, n in zip(fields, problem2.your_ticket)
        if name.startswith('departure')
    ]
    assert len(departure_values) == 6
    print(math.prod(departure_values))
    