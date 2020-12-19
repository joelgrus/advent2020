from __future__ import annotations
from typing import NamedTuple, List, Optional, Tuple, Iterator
from collections import deque

class Rule(NamedTuple):
    id: int
    literal: Optional[str] = None
    subrules: List[List[int]] = []

    @staticmethod
    def parse(line: str) -> Rule:
        rule_id, rest = line.strip().split(": ")
        if rest.startswith('"'):
            return Rule(id=int(rule_id), literal=rest[1:-1])
        
        if "|" in rest:
            parts = rest.split(" | ")
        else:
            parts = [rest]

        return Rule(id=int(rule_id), 
                    subrules=[[int(n) for n in part.split()] for part in parts])


def check(s: str, rules: List[Rule]) -> bool:
    """
    Returns True if s is a match for rules[0]
    """
    # queue of pairs (remaining string, remaining rules)
    q = deque([(s, [0])])
    
    while q:
        # take from the queue
        s, rule_ids = q.popleft()

        # consumed the whole string and all the rules,
        # so that's a match
        if not s and not rule_ids:
            return True

        # consumed the string or the rules but not both, 
        # so this is a dead end, forget it and continue
        elif not s or not rule_ids:
            continue

        # each rule can match at most 1 character
        # so if we have more than that it's definitely not a match
        elif len(rule_ids) > len(s):
            continue

        # have both s and rule_ids. So let's try the first rule in our ids
        rule = rules[rule_ids[0]]
        rule_ids = rule_ids[1:]

        # first rule is literal, so if it matches the first character,
        # then add the rest of the string and the rest of the rules to the queue
        if rule.literal and s[0] == rule.literal:
            q.append((s[1:], rule_ids))

        # otherwise, I have one more sequences of subrules,
        # for each of those sequences, I prepend it to the remaining rule_ids
        # and add that new list of rule ids to the queue with s
        else:
            for subrule_ids in rule.subrules:
                q.append((s, subrule_ids + rule_ids))


    # queue is exhausted, never found a match, so return False
    return False


def parse(raw: str):
    raw_rules, raw_strings = raw.split("\n\n")
    rules = [Rule.parse(rr) for rr in raw_rules.split("\n")]
    rules.sort()  # <--- ARGH
    assert all(rule.id == i for i, rule in enumerate(rules))
    strings = raw_strings.split("\n")
    return rules, strings


#
# unit tests
#

RAW = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

RULES, STRINGS = parse(RAW)

assert sum(check(s, RULES) for s in STRINGS) == 2

#
# problem
# 

with open('inputs/day19.txt') as f:
    raw = f.read()
rules, strings = parse(raw)

# good = 0
# for i, s in enumerate(strings):
#     print(i, s)
#     if check(s, rules):
#         good += 1

# print(good)

# part 2
rules[8] = Rule.parse("8: 42 | 42 8")
rules[11] = Rule.parse("11: 42 31 | 42 11 31")

good = 0
for i, s in enumerate(strings):
    print(i, s)
    if check(s, rules):
        good += 1

print(good)