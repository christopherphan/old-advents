"""Solution to Day 14 of 2015 Advent of Code."""
from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Collection
from dataclasses import dataclass
from sys import argv
from typing import Final

from rich.console import Console

INPUT_PATTERN: Final[re.Pattern] = re.compile(
    r"([A-Za-z]+) can fly (\d+) km/s for (\d+) seconds,"
    + r" but then must rest for (\d+) seconds."
)


@dataclass
class Reindeer:
    """Represent a reindeer."""

    name: str
    speed: int
    fly_time: int
    rest_time: int

    @classmethod
    def from_input(cls: type[Reindeer], line: str) -> Reindeer:
        """Create a reindeer from a line of puzzle input."""
        if m := INPUT_PATTERN.match(line.strip()):
            return cls(m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)))
        else:
            raise ValueError(f"Invalid input: {line}")

    def distance(self: Reindeer, t: int) -> int:
        """Determine the distance travelled by time t."""
        cycles, extra = divmod(t, self.fly_time + self.rest_time)
        return self.speed * (self.fly_time * cycles + min(extra, self.fly_time))


def winning_distance(t: int, reindeer: Collection[Reindeer]) -> int:
    """Return the farthest distance any reindeers cover by time t."""
    return max(r.distance(t) for r in reindeer)


def winning_points(t: int, reindeer: Collection[Reindeer]) -> int:
    """Return the number of points the winning reindeer will have in Part 2."""
    score: dict[str, int] = {r.name: 0 for r in reindeer}
    for k in range(1, t + 1):
        current_distances: defaultdict[int, list[str]] = defaultdict(list)
        for r in reindeer:
            current_distances[r.distance(k)].append(r.name)
        for name in current_distances[max(current_distances.keys())]:
            score[name] += 1
    return max(score.values())


def parse_input(text: str) -> list[Reindeer]:
    """Parse the puzzle input and return a set of Reindeer."""
    return [Reindeer.from_input(line) for line in text.splitlines()]


if __name__ == "__main__":
    c = Console()
    if len(argv) == 1:
        c.print(f"[white on red]Usage:[/] [yellow on black]{argv[0]}[/] filename")
    else:
        with open(argv[1], "rt") as infile:
            reindeer_list = parse_input(infile.read())
        c.print(
            "[magenta on black]Part 0:[/]"
            + f" [yellow on black]Dist: {winning_distance(1000, reindeer_list)}, "
            + f"Points: {winning_points(1000, reindeer_list)}[/]"
        )
        c.print(
            "[magenta on black]Part 1:[/]"
            + f" [yellow on black]{winning_distance(2503, reindeer_list)}[/]"
        )
        c.print(
            "[magenta on black]Part 2:[/]"
            + f" [yellow on black]{winning_points(2503, reindeer_list)}[/]"
        )
