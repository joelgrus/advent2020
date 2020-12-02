from __future__ import annotations

from typing import NamedTuple

PASSWORDS = [
    "1-3 a: abcde",
    "1-3 b: cdefg",
    "2-9 c: ccccccccc"
]

class Password(NamedTuple):
    lo: int
    hi: int
    char: str
    password: str

    def is_valid(self) -> bool:
        return self.lo <= self.password.count(self.char) <= self.hi

    def is_valid2(self) -> bool:
        is_lo = self.password[self.lo - 1] == self.char
        is_hi = self.password[self.hi - 1] == self.char

        return is_lo != is_hi

    @staticmethod
    def from_line(line: str) -> Password:
        """
            "1-3 a: abcde",
        """
        counts, char, password = line.strip().split()
        lo, hi = [int(n) for n in counts.split("-")]
        char = char[0]
        return Password(lo, hi, char, password)


with open('inputs/day02.txt') as f:
    passwords = [Password.from_line(line) for line in f]
    print(sum(pw.is_valid2() for pw in passwords))

