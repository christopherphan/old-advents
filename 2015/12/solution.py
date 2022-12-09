"""Solution to Day 12 of 2015 Advent of Code."""

import json
from sys import argv

from rich.console import Console


def find_sum(x: int | str | list | dict, ignore_red: bool = False) -> int:
    """Find the sum of all numbers in x."""
    if isinstance(x, int):
        return x
    if isinstance(x, str):
        return 0  # We are told not to consider digits inside strings
    if isinstance(x, list):
        return sum(find_sum(k, ignore_red) for k in x)
    if isinstance(x, dict):
        vals = x.values()
        if not ignore_red or "red" not in vals:
            return sum(
                find_sum(k, ignore_red) for k in vals
            )  # JSON keys are strings, which we ignore
    return 0


def test(c: Console):
    """Test the four example inputs."""
    objs: list[
        str
    ] = """[1,2,3]
    {"a":2,"b":4}
    [[[3]]]
    {"a":{"b":4},"c":-1}
    {"a":[-1,1]}
    [-1,{"a":1}]
    []
    {}
    [1,{"c":"red","b":2},3]
    {"d":"red","e":[1,2,3,4],"f":5}
    [1,"red",5]""".splitlines()

    for k in objs:
        data = json.loads(k)
        val1 = find_sum(data)
        val2 = find_sum(data, True)
        c.print(f"[magenta on black]{k.strip()}[/]:")
        c.print(f"\t[green on black]Part 1:[/] [yellow on black]{val1}[/]")
        c.print(f"\t[green on black]Part 2:[/] [yellow on black]{val2}[/]")


if __name__ == "__main__":
    c = Console()
    if len(argv) == 1:
        test(c)
    else:
        with open(argv[1], "rt") as infile:
            data = json.load(infile)
        c.print(f"[green on black]Part 1:[/] [yellow on black]{find_sum(data)}[/]")
        c.print(
            f"[green on black]Part 2:[/] [yellow on black]{find_sum(data, True)}[/]"
        )
