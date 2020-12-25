from __future__ import annotations

from typing import Iterator
"""
The handshake used by the card and the door involves an operation 
that transforms a subject number. To transform a subject number, 
start with the value 1. Then, a number of times called the loop size, 
perform the following steps:

Set the value to itself multiplied by the subject number.
Set the value to the remainder after dividing the value by 20201227.
"""

def handshakes(subject_number: int = 7) -> Iterator[int]:
    value = 1
    while True:
        yield value
        value = (value * subject_number) % 20201227

def handshake(loop_number: int, subject_number: int = 7) -> int:
    for i, n in enumerate(handshakes(subject_number)):
        if i == loop_number:
            return n
    raise RuntimeError()

def find_loop_number(public_key: int, subject_number: int = 7) -> int:
    for i, n in enumerate(handshakes(subject_number)):
        if n == public_key:
            return i
    raise RuntimeError()


#
# unit tests
#

assert find_loop_number(5764801) == 8
assert find_loop_number(17807724) == 11

#
# problem
#

door_key = 12578151
card_key = 5051300

door_number = find_loop_number(door_key)
print(handshake(door_number, card_key))

card_number = find_loop_number(card_key)
print(handshake(card_number, door_key))
