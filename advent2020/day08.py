from __future__ import annotations

from typing import NamedTuple, List

class Instruction(NamedTuple):
    op: str
    arg: int

    @staticmethod
    def parse(line: str) -> Instruction:
        op, arg = line.strip().split()
        return Instruction(op, int(arg))


class Booter:
    def __init__(self, instructions: List[Instruction]) -> None:
        self.instructions = instructions
        self.accumulator = 0
        self.idx = 0

    def execute_one(self) -> None:
        op, arg = self.instructions[self.idx]

        if op == 'acc':
            self.accumulator += arg
            self.idx += 1
        elif op == 'jmp':
            self.idx += arg
        elif op == 'nop':
            self.idx += 1
        else:
            raise ValueError(f"unknown op: {op}")

    def run_until_repeat(self) -> None:
        executed = set()

        while self.idx not in executed:
            executed.add(self.idx)
            self.execute_one()

    def does_terminate(self) -> bool:
        executed = set()

        while self.idx not in executed:
            if self.idx == len(self.instructions):
                return True

            executed.add(self.idx)
            self.execute_one()

        return False


def find_terminator(instructions: List[Instruction]) -> int:
    for i, (op, arg) in enumerate(instructions):
        subbed = instructions[:]

        if op == 'nop':
            subbed[i] = Instruction('jmp', arg)
        elif op == 'jmp':
            subbed[i] = Instruction('nop', arg)
        else:
            continue

        booter = Booter(subbed)

        if booter.does_terminate():
            return booter.accumulator

    raise RuntimeError("never terminated")

#
# UNIT TESTS
#

RAW = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

INSTRUCTIONS = [Instruction.parse(line) for line in RAW.split("\n")]

BOOTER = Booter(INSTRUCTIONS)
BOOTER.run_until_repeat()
assert BOOTER.accumulator == 5

assert find_terminator(INSTRUCTIONS) == 8

#
# PROBLEM
#

with open('inputs/day08.txt') as f:
    raw = f.read()

instructions = [Instruction.parse(line) for line in raw.split("\n")]
booter = Booter(instructions)
booter.run_until_repeat()
print(booter.accumulator)
print(find_terminator(instructions))
