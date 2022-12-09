"""Solution to Day 9 of 2015 Advent of Code."""

from __future__ import annotations

from itertools import combinations, permutations
from sys import argv

from rich.console import Console

from _resources import PuzzleSolution


def parse_line(text: str) -> tuple[frozenset[str], int]:
    """Parse a line from the input file."""
    location_part, cost = text.split(" = ", maxsplit=1)
    start, end = location_part.split(" to ", maxsplit=1)
    return frozenset([start, end]), int(cost)


def parse_input(text: str) -> tuple[set[str], dict[frozenset[str], int]]:
    """Parse the input file."""
    locations: set[str] = set()
    costs: dict[frozenset[str], int] = {}
    for line in text.splitlines():
        key, value = parse_line(line)
        locations |= key
        costs[key] = value
    return locations, costs


def route_cost(places: list[str], cost_data: dict[frozenset[str], int]) -> int:
    """Return the cost of a route."""
    return sum(cost_data[frozenset(pair)] for pair in zip(places[:-1], places[1:]))


def all_route_costs(locations: set[str], costs: dict[frozenset[str], int]) -> list[int]:
    """Part 1 of puzzle."""
    return [
        route_cost([endpoints[0]] + list(middle) + [endpoints[1]], costs)
        for endpoints in combinations(locations, 2)
        for middle in permutations(locations - set(endpoints))
    ]


def process_input(text: str) -> dict:
    """Process the input and return a list of costs."""
    return {"costs": all_route_costs(*parse_input(text))}


pz = PuzzleSolution.from_parser(process_input)


@pz.register_result_function("Part 1")
def part1(data: dict) -> str:
    """Return the minimum route cost."""
    return str(min(data["costs"]))


@pz.register_result_function("Part 2")
def part2(data: dict) -> str:
    """Return the maximum route cost."""
    return str(max(data["costs"]))


if __name__ == "__main__":
    pz.add_input("example_input.txt", "Example input")
    pz.add_input("input.txt", "Puzzle input")

    c = Console()
    pz.report_results(c, argv[0])
