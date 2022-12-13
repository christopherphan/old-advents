"""Solution to Day 16 of 2015 Advent of Code."""
from __future__ import annotations

import re
from typing import Final, NamedTuple

from rich.console import Console

SUE_PATTERN: Final[re.Pattern] = re.compile(
    r"Sue (\d+): ([a-z]+): (\d+), ([a-z]+): (\d+), ([a-z]+): (\d+)"
)


class Sue(NamedTuple):
    """Represents an Aunt Sue."""

    num: int
    detectables: dict[str, int]

    @classmethod
    def parse_line(cls: type[Sue], line: str) -> Sue:
        """Parse a line of the Sue data to get a Sue."""
        if (m := SUE_PATTERN.match(line)) is None:
            raise ValueError("Doesn't match the pattern.")
        return cls(
            int(m.group(1)),
            {
                m.group(2 * k + 2).strip(): int(m.group(2 * k + 3).strip())
                for k in range(3)
            },
        )

    def match(self: Sue, gift_data: dict[str, int], part2: bool = False) -> bool:
        """Determine if this Sue matches the gift data."""
        if not part2:
            return all(
                value == gift_data[key] for key, value in self.detectables.items()
            )
        else:
            return all(
                (
                    value > gift_data[key]
                    if key in ["cats", "trees"]
                    else value < gift_data[key]
                    if key in ["pomeranians", "goldfish"]
                    else value == gift_data[key]
                )
                for key, value in self.detectables.items()
            )


def parse_gift_data(data: str) -> dict[str, int]:
    """Parse the gift data information."""
    return {
        (sp := line.split(":", maxsplit=1))[0].strip(): int(sp[1].strip())
        for line in data.splitlines()
    }


if __name__ == "__main__":
    c = Console()

    with open("gift_data.txt", "rt") as infile:
        gift_data = parse_gift_data(infile.read())

    with open("input.txt", "rt") as infile:
        raw_lines = infile.read().splitlines()

    for line in raw_lines:
        if (s := Sue.parse_line(line)).match(gift_data):
            c.print(f"[white on dark_green]Part 1:[/] [yellow on black]{s.num}[/]")
        if s.match(gift_data, True):
            c.print(f"[white on dark_red]Part 2:[/] [cyan on black]{s.num}[/]")
