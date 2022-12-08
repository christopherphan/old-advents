"""Solution to Day 6 of the 2015 Advent of Code."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from sys import argv
from typing import Final

from _resources import Console, main, make_reporter, print_help

INSTR_PATTERN: Final[re.Pattern] = re.compile(
    r"([a-z ]+) (\d+),(\d+) through (\d+),(\d+)"
)

PART1_COMMANDS: Final[dict[str, Callable[[int], int]]] = {
    "turn on": (lambda x: 1),
    "turn off": (lambda x: 0),
    "toggle": (lambda x: 1 if x == 0 else 0),
}

PART2_COMMANDS: Final[dict[str, Callable[[int], int]]] = {
    "turn on": (lambda x: x + 1),
    "turn off": (lambda x: max(0, x - 1)),
    "toggle": (lambda x: x + 2),
}


@dataclass
class LightCommand:
    """Represents an operation on a LightGrid."""

    corner1: tuple[int, int]
    corner2: tuple[int, int]
    state_change: Callable[[int], int]

    @classmethod
    def parse_line(
        cls: type[LightCommand],
        command_dict: dict[str, Callable[[int], int]],
        text: str,
    ) -> LightCommand:
        """Interpret a text command."""
        if m := INSTR_PATTERN.match(text):
            return cls(
                (int(m.group(2)), int(m.group(3))),
                (int(m.group(4)), int(m.group(5))),
                command_dict.get(m.group(1), lambda x: x),
            )
        else:
            return cls((0, 0), (0, 0), lambda x: x)


class LightGrid:
    """Represents the state of the lights."""

    def __init__(self: LightGrid) -> None:
        """Initialize object (all turned off)."""
        self.light_state = [[0 for _ in range(1_000)] for _2 in range(1_000)]

    @property
    def total_brightness(self: LightGrid) -> int:
        """Return the number of lit lights."""
        return sum(sum(row) for row in self.light_state)

    def run_command(self: LightGrid, cmd: LightCommand) -> None:
        """Apply a LightCommand to the grid."""
        row_min = min(cmd.corner1[0], cmd.corner2[0])
        row_max = max(cmd.corner1[0], cmd.corner2[0])
        col_min = min(cmd.corner1[1], cmd.corner2[1])
        col_max = max(cmd.corner1[1], cmd.corner2[1])
        for row in range(row_min, row_max + 1):
            for col in range(col_min, col_max + 1):
                self.light_state[row][col] = cmd.state_change(
                    self.light_state[row][col]
                )


def create_grid(cmd_dict: dict[str, Callable[[int], int]], text: str) -> LightGrid:
    """Apply a list of text commands to a new LightGrid."""
    lights = LightGrid()
    for line in text.splitlines():
        lights.run_command(LightCommand.parse_line(cmd_dict, line))
    return lights


def soln_fcn(cmd_dict: dict[str, Callable[[int], int]]) -> Callable[[str], str]:
    """Create a function applying the command dictionary to a set of text instructions."""

    def ret_fcn(text: str) -> str:
        return str(create_grid(cmd_dict, text).total_brightness)

    return ret_fcn


RESULT_FUNCTIONS: Final[dict[str, Callable[[str], str]]] = {
    "Part 1": soln_fcn(PART1_COMMANDS),
    "Part 2": soln_fcn(PART2_COMMANDS),
}

if __name__ == "__main__":
    main(argv, print_help, make_reporter(lambda x: x, RESULT_FUNCTIONS))
