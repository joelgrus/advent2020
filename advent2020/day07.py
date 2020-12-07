from typing import NamedTuple, Dict, List, Tuple
import re
from collections import defaultdict

RAW = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

RAW2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""


class Bag(NamedTuple):
    color: str
    contains: Dict[str, int]


def parse_line(line: str) -> Bag:
    part1, part2 = line.split(" contain ")
    color = part1[:-5]

    part2 = part2.rstrip(".")
    if part2 == "no other bags":
        return Bag(color, {})
    
    contains = {}

    contained = part2.split(", ")
    for subbag in contained:
        subbag = re.sub(r"bags?$", "", subbag)
        first_space = subbag.find(" ")
        count = int(subbag[:first_space].strip())
        color2 = subbag[first_space:].strip()
        contains[color2] = count
    return Bag(color, contains)

def make_bags(raw: str) -> List[Bag]:
    return [parse_line(line) for line in raw.split("\n")]

def parents(bags: List[Bag]) -> Dict[str, List[str]]:
    ic = defaultdict(list)
    for bag in bags:
        for child in bag.contains:
            ic[child].append(bag.color)
    return ic

def can_eventually_contain(bags: List[Bag], color: str) -> List[str]:
    parent_map = parents(bags)
    
    check_me = [color]
    can_contain = set()

    while check_me:
        child = check_me.pop()
        for parent in parent_map.get(child, []):
            if parent not in can_contain:
                can_contain.add(parent)
                check_me.append(parent)

    return list(can_contain)

def num_bags_inside(
    bags: List[Bag], 
    color: str
) -> int:
    by_color = {bag.color: bag for bag in bags}

    num_bags = 0
    stack: List[Tuple[str, int]] = [(color, 1)]
    while stack:
        next_color, multiplier = stack.pop()
        bag = by_color[next_color]
        for child, count in bag.contains.items():
            num_bags += multiplier * count
            stack.append((child, count * multiplier))
    return num_bags

BAGS1 = make_bags(RAW)
BAGS2 = make_bags(RAW2)




with open('inputs/day07.txt') as f:
    raw = f.read()
    bags = make_bags(raw)
    print(len(can_eventually_contain(bags, 'shiny gold')))
    print(num_bags_inside(bags, "shiny gold"))