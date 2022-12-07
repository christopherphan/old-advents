"""Solution for Day 3 of the 2015 Advent of Code."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from sys import argv
from typing import Final

from rich.console import Console

from _resources import interactive_loop, main, report_results


@dataclass(frozen=True)
class Position:
    """Represents a position, absolute or relative."""

    x: int
    y: int

    def __add__(self: Position, other):
        """Return ``self + other``."""
        if isinstance(other, Position):
            return self.__class__(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented


DIRECTIONS: Final[dict[str, Position]] = {
    ">": Position(1, 0),
    "<": Position(-1, 0),
    "^": Position(0, 1),
    "v": Position(0, -1),
}


def parse_input(text: str) -> list[Position]:
    """Parse input and list as a series of Position objects."""
    return [DIRECTIONS[char] for char in text if char in DIRECTIONS]


def places_visited(
    moves: list[Position], start: Position | None = None, num_santas: int = 1
) -> list[Position]:
    """Process a sequence of moves and return the list of locations visited."""
    outlist: dict[int, list[Position]] = {k: [] for k in range(num_santas)}
    if start is None:
        for val in outlist.values():
            val.append(Position(0, 0))
    else:
        for val in outlist.values():
            val.append(start)
    for idx, m in enumerate(moves):
        outlist[idx % num_santas].append(outlist[idx % num_santas][-1] + m)
    ret_val = []
    for val in outlist.values():
        ret_val.extend(val)
    return ret_val


def num_places_visited(places: list[Position]) -> str:
    """Return the number of houses visited."""
    return f"{len(set(places))} houses"


def part1(moves: list[Position]) -> str:
    """Provide answer for part 1."""
    return num_places_visited(places_visited(moves))


def part2(moves: list[Position]) -> str:
    """Provide answer for part 2."""
    return num_places_visited(places_visited(moves, num_santas=2))


RESULT_FCN: Final[dict[str, Callable[[list[Position]], str]]] = {
    "Part 1": part1,
    "Part 2": part2,
}


def file_fcn(text: str, c: Console) -> None:
    """Parse and report based on the contents of a string."""
    report_results(c, parse_input, RESULT_FCN, text)


if __name__ == "__main__":
    main(argv, interactive_loop(parse_input, RESULT_FCN), file_fcn)
