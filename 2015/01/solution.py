"""Solution to Day 1 of 2015 Advent of Code."""

from collections import Counter
from sys import argv

from rich.console import Console


def process_text(text: str) -> int:
    """Count the characters ``(`` and ``)`` and give the result."""
    ctr = Counter(text)
    return ctr["("] - ctr[")"]


def when_first_floor(text: str) -> int:
    """Provide the part 2 solution."""
    floor = 0
    for idx, char in enumerate(text):
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1
        if floor == -1:
            return idx + 1
    return -1


def process_and_show(text: str, c: Console) -> None:
    """Process the text and show the solution to both parts."""
    c.print(f"Part 1: [yellow on black]{process_text(text)}[/]")
    if (moves := when_first_floor(text)) != -1:
        c.print(f"Part 2: [yellow on black]{moves}[/]")
    else:
        c.print("Part 2: [yellow on black]Never in basement[/]")


def interactive_loop(c: Console) -> None:
    """Process user input interactively."""
    while text := c.input("[magenta on black]Input [/](blank to exit): "):
        process_and_show(text, c)


if __name__ == "__main__":
    c = Console()
    if len(argv) == 1:
        interactive_loop(c)
    else:
        with open(argv[1], "rt") as infile:
            text = infile.read()
        process_and_show(text, c)
