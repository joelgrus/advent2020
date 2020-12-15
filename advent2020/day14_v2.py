from __future__ import annotations
from os import umask
from typing import Dict, List, Iterator, Iterable
from collections import defaultdict
import itertools

def to_binary(value: int, num_digits: int = 36) -> str:
    return f"{value:36b}".replace(" ", "0")

def apply_mask(value: int, mask: str) -> int:
    outdigits = []

    for vb, mb in zip(to_binary(value), mask):
        if mb == 'X':
            outdigits.append(vb)
        else:
            outdigits.append(mb)

    return int("".join(outdigits), 2)


def apply_multi_mask(value: int, mask: str) -> Iterator[int]:
    binary = to_binary(value)

    xs = [i for i, c in enumerate(mask) if c == 'X'] 
    sub_values = [['0', '1'] for _ in xs]
    for choice in itertools.product(*sub_values):
        new_binary = list(binary)
        it = iter(choice)

        for i, (vb, mb) in enumerate(zip(binary, mask)):
            if mb == '0':
                pass 
            elif mb == '1':
                new_binary[i] = '1'
            else:
                new_binary[i] = next(it)

        yield int(''.join(new_binary), 2)



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

            value = apply_mask(value, mask)

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