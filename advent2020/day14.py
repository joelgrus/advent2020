from __future__ import annotations
from os import umask
from typing import Dict, List, Iterator, Iterable
from collections import defaultdict
import itertools

def to_binary(value: int, num_digits: int = 36) -> List[int]:
    digits = []
    for _ in range(num_digits):
        digits.append(value % 2)
        value = value // 2
    return list(reversed(digits))

def apply_mask(value: int, mask: str) -> int:
    """do not use, doesn't work"""
    output = 0
    for i, m in enumerate(reversed(mask)):
        if m == '1':
            output += 2 ** i
        elif m == '0':
            pass 
        else:
            output += (2 ** i) & value

    return output

def apply_mask2(value: int, mask: str) -> int:
    digits = to_binary(value)
    output = 0

    for i, (digit, m) in enumerate(zip(digits, mask)):
        if m == '1':
            digits[i] = 1
        elif m == '0':
            digits[i] = 0
    
    return sum(digit * (2 ** i) for i, digit in enumerate(reversed(digits)))

def apply_multi_mask(value: int, mask: str) -> Iterator[int]:
    digits = to_binary(value)
    output = 0

    xs = [i for i, c in enumerate(mask) if c == 'X'] 
    sub_values = [[0, 1] for _ in xs]
    for choice in itertools.product(*sub_values):
        print(choice)
        new_digits = digits[:]
        it = iter(choice)
        for i, (digit, m) in enumerate(zip(digits, mask)):
            if m == '0':
                pass  # leave the digit as is
            elif m == '1':
                new_digits[i] = 1
            else:
                new_digits[i] = next(it)
        
        yield sum(digit * (2 ** i) for i, digit in enumerate(reversed(new_digits)))


def run(program: List[str]) -> Dict[int, int]:
    memory = defaultdict(int)
    mask = None

    for line in program:
        if line.startswith("mask"):
            mask = line.split(" = ")[-1]
        else:
            mem, value_s = line.split(" = ")
            value = int(value_s)
            pos = int(mem[4:-1])

            value = apply_mask2(value, mask)

            memory[pos] = value


    return memory


def run2(program: List[str]) -> Dict[int, int]:
    mask = None
    memory = defaultdict(int)

    for line in program:
        print(line)
        if line.startswith("mask"):
            mask = line.split(" = ")[-1]
        else:
            mem, value_s = line.split(" = ")
            value = int(value_s)
            pos = int(mem[4:-1])

            print(pos, value)

            for pos2 in apply_multi_mask(pos, mask):
                memory[pos2] = value

    return memory
    

#
# unit tests
#

RAW = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

PROGRAM = RAW.split("\n")
MEMORY = run(PROGRAM)
assert sum(MEMORY.values()) == 165

RAW2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

PROGRAM2 = RAW2.split("\n")
MEMORY2 = run2(PROGRAM2)
assert sum(MEMORY2.values()) == 208

# 
# problem
#

with open('inputs/day14.txt') as f:
    program = [line for line in f]
    memory = run(program)
    print(sum(memory.values()))

    memory2 = run2(program)
    print(sum(memory2.values()))