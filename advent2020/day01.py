from typing import List

INPUTS = [
    1721,
    979,
    366,
    299,
    675,
    1456,
]

def find_product(inputs: List[int]) -> int:
    """
    Find the two elements that add up to 2020
    and return their product
    """
    needs = {2020 - i for i in inputs}

    for i in inputs:
        if i in needs:
            return i * (2020-i)

assert find_product(INPUTS) == 514579

def find_product3(inputs: List[int]) -> int:
    """
    Find the two elements that add up to 2020
    and return their product
    """
    needs = {2020 - i - j: (i, j)
             for i in inputs
             for j in inputs
             if i != j}

    for i in inputs:
        if i in needs:
            j, k = needs[i]
            return i * j * k

assert find_product3(INPUTS) == 241861950

with open("inputs/day01.txt") as f:
    inputs = [int(line.strip()) for line in f]
    print(find_product3(inputs))