from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re

Expression = List[str]

def evaluate(expression: Expression) -> int:
    """
    This is for an expression with no parentheses
    """
    value = int(expression[0])
    for i in range(1, len(expression), 2):
        op = expression[i]
        if op == "+":
            value = value + int(expression[i+1])
        elif op == "*":
            value = value * int(expression[i+1])
        else:
            raise ValueError(f"bad op: {op}")
    
    return value

# Regex to match open-parens ... closed-parens
# with no parens in between 
rgx = r"\([^\(]+?\)"

def evaluate_raw(raw: str) -> int:
    while (match := re.search(rgx, raw)):
        value = evaluate(match.group()[1:-1].split())
        raw = raw[:match.start()] + str(value) + raw[match.end():]
    else:
        tokens = raw.split()
        return evaluate(tokens)


def evaluate2(expression: Expression) -> int:
    """again assumes expression has no parens"""
    while len(expression) > 1:
        if "+" in expression:
            # find the plus and use it on the surrounding numbers
            i = expression.index("+")
            new_val = int(expression[i-1]) + int(expression[i+1])
            # and then put that result back
            expression = expression[:i-1] + [str(new_val)] + expression[i+2:]
        else:
            return evaluate(expression)

    return int(expression[0])


def evaluate_raw2(raw: str) -> int:
    while (match := re.search(rgx, raw)):
        value = evaluate2(match.group()[1:-1].split())
        raw = raw[:match.start()] + str(value) + raw[match.end():]
    else:
        tokens = raw.split()
        return evaluate2(tokens)


#
# unit tests
#

RAW = "1 + 2 * 3 + 4 * 5 + 6"
assert evaluate_raw(RAW) == 71
assert evaluate_raw2(RAW) == 231

RAW2 = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
assert evaluate_raw(RAW2) == 13632
assert evaluate_raw2(RAW2) == 23340

#
# problem
#

with open('inputs/day18.txt') as f:
    raw = f.read()
    lines = raw.split("\n")
    print(sum(evaluate_raw(line) for line in lines))
    print(sum(evaluate_raw2(line) for line in lines))