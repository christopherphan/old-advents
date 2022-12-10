"""Solution for day 13 of 2015 Advent of Code."""

from __future__ import annotations

import re
from collections.abc import Callable, Collection, Sequence
from dataclasses import dataclass
from itertools import combinations, permutations
from sys import argv
from typing import Final

from rich.console import Console

RULE: Final[re.Pattern] = re.compile(
    r"([a-zA-Z]+) would ([a-z]+) (\d+) happiness units "
    + r"by sitting next to ([a-zA-Z]+)."
)


@dataclass(frozen=True)
class Effect:
    """Represent an effect of one person on another."""

    guest: str
    neighbor: str
    change: int

    @classmethod
    def from_text(cls: type[Effect], text: str) -> Effect:
        """Create a rule based on a line of puzzle input."""
        s_text = text.strip()
        if not (m := RULE.match(s_text)):
            raise ValueError(f"Not a valid rule: {s_text}")
        change: int = int(m.group(3))
        if m.group(2) == "lose":
            change = -change
        return cls(m.group(1), m.group(4), change)

    def evaluate_on_pair(self: Effect, pair: tuple[str, str]) -> int:
        """Evaluate the effect of this rule on a given pair."""
        if set(pair) == {self.guest, self.neighbor}:
            return self.change
        else:
            return 0


def create_pair_evaluator(effects: Collection[Effect]) -> Callable[[str, str], int]:
    """Create a function that evaluates the effect of pairs seated adjecent."""
    evaluator_cache: dict[frozenset[str], int] = {}

    def evaluator(guest1: str, guest2: str) -> int:
        fz = frozenset([guest1, guest2])
        if fz not in evaluator_cache:
            evaluator_cache[fz] = sum(
                eff.evaluate_on_pair((guest1, guest2)) for eff in effects
            )
        return evaluator_cache[fz]

    return evaluator


def evaluate_seating_arrangment(
    seats: Sequence[str], evaluator: Callable[[str, str], int]
) -> int:
    """Return the value of a seating arrangement."""
    return sum(evaluator(*pair) for pair in zip(seats, list(seats[1:]) + [seats[0]]))


def find_best_arrangment(
    guests: Sequence[str], evaluator: Callable[[str, str], int]
) -> int:
    """Return the value of the best arrangment."""
    guest_list = list(guests)
    return max(
        evaluate_seating_arrangment(
            [guest_list[0]] + [endpt[0]] + list(rest) + [endpt[1]], evaluator
        )
        # The seating arrangements are invariant under rotation and change of
        # orientation. Hence, we can assume that the same guest is seated at the start
        # of the list, and each permutation of the other guests AB___C is equivalent
        # to AC___B.
        for endpt in combinations(guest_list[1:], 2)
        for rest in permutations(set(guest_list[1:]) - set(endpt))
    )


def parse_input(text: str) -> tuple[set[str], Callable[[str, str], int]]:
    """Parse the input."""
    guests: set[str] = set()
    effects: list[Effect] = []
    for line in text.splitlines():
        new_eff = Effect.from_text(line)
        guests.add(new_eff.guest)
        guests.add(new_eff.neighbor)
        effects.append(new_eff)
    return guests, create_pair_evaluator(effects)


if __name__ == "__main__":
    c = Console()
    if len(argv) == 1:
        c.print(f"[white on red]Usage[/]: [yellow on black]{argv[0]}[/] filename")
    else:
        with open(argv[1], "rt") as infile:
            guests, evaluator = parse_input(infile.read())
        c.print(
            "[magenta on black]Part 1:[/] "
            + f"[yellow on black]{find_best_arrangment(list(guests), evaluator)}[/]"
        )
        # The way I designed my program, you don't need to include zero effects
        # on the effects list.
        guests.add("SELF")
        c.print(
            "[magenta on black]Part 2:[/] "
            + f"[yellow on black]{find_best_arrangment(list(guests), evaluator)}[/]"
        )
