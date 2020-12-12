"""Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing."""

from __future__ import annotations
from typing import NamedTuple
from dataclasses import dataclass

class Action(NamedTuple):
    action: str
    amount: int

    @staticmethod
    def parse(raw: str):
        return Action(raw[0], int(raw[1:]))

@dataclass
class Ship:
    x: int = 0
    y: int = 0 
    heading: int = 0

    def move(self, action: Action) -> None:
        if action.action == 'N':
            self.y += action.amount
        elif action.action == 'S':
            self.y -= action.amount
        elif action.action == 'E':
            self.x += action.amount
        elif action.action == 'W':
            self.x -= action.amount
        elif action.action == 'L':
            self.heading = (self.heading + action.amount) % 360
        elif action.action == 'R':
            self.heading = (self.heading - action.amount) % 360
        elif action.action == 'F':
            if self.heading == 0:
                self.x += action.amount 
            elif self.heading == 90:
                self.y += action.amount
            elif self.heading == 180:
                self.x -= action.amount
            elif self.heading == 270:
                self.y -= action.amount
            else:
                raise ValueError(f"bad heading {self.heading}")
        else:
            raise ValueError(f"unknown action {action}")            


@dataclass
class ShipAndWaypoint:
    ship_x: int = 0
    ship_y: int = 0 
    ship_heading: int = 0

    waypoint_x: int = 10
    waypoint_y: int = 1

    def move(self, action: Action) -> None:
        if action.action == 'N':
            self.waypoint_y += action.amount
        elif action.action == 'S':
            self.waypoint_y -= action.amount
        elif action.action == 'E':
            self.waypoint_x += action.amount
        elif action.action == 'W':
            self.waypoint_x -= action.amount
        elif action.action == 'L':
            # rotate the waypoint around the ship the given number of degrees
            for _ in range(action.amount // 90):
                self.waypoint_x, self.waypoint_y = -self.waypoint_y, self.waypoint_x
        elif action.action == 'R':
            for _ in range(action.amount // 90):
                self.waypoint_x, self.waypoint_y = self.waypoint_y, -self.waypoint_x

        elif action.action == 'F':
            self.ship_x += action.amount * self.waypoint_x
            self.ship_y += action.amount * self.waypoint_y
        else:
            raise ValueError(f"unknown action {action}")            


# 
# unit tests
#

RAW = """F10
N3
F7
R90
F11"""

ACTIONS = [Action.parse(line) for line in RAW.split("\n")]
SHIP = Ship()

for action in ACTIONS:
    SHIP.move(action)

assert SHIP.x == 17
assert SHIP.y == -8

SAW = ShipAndWaypoint()
for action in ACTIONS:
    SAW.move(action)

assert SAW.ship_x == 214
assert SAW.ship_y == -72

#
# problem
#

with open('inputs/day12.txt') as f:
    raw = f.read()
    actions = [Action.parse(line) for line in raw.split("\n")]
    ship = Ship()
    for action in actions:
        ship.move(action)
    print(abs(ship.x) + abs(ship.y))

    saw = ShipAndWaypoint()
    for action in actions:
        saw.move(action)
    print(abs(saw.ship_x) + abs(saw.ship_y))
