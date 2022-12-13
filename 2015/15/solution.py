"""Solution to Day 15 of 2015 Advent of Code."""

from __future__ import annotations

import itertools
import random
import re
from collections.abc import Collection, Sequence
from math import ceil, floor
from sys import argv
from typing import Final, NamedTuple

from rich.console import Console

INPUT_PATTERN: Final[re.Pattern] = re.compile(
    r"([a-zA-Z]+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+),"
    + r" texture (-?\d+), calories (\d+)"
)

ATTRIBS: Final[list[str]] = ["capacity", "durability", "flavor", "texture"]


class Ingredient(NamedTuple):
    """Represent an ingredient."""

    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @classmethod
    def from_input(cls: type[Ingredient], text: str) -> Ingredient:
        """Create an ingredient from a line of puzzle input."""
        if (m := INPUT_PATTERN.match(text)) is None:
            raise ValueError(f"Invalid input: {text}")
        vals = m.groups()
        return cls(vals[0], *[int(k) for k in vals[1:]])


class IngredientCoeffs(NamedTuple):
    """Represent info about linear equations in the ingredients."""

    fixed: Ingredient
    free: list[Ingredient]
    const: dict[str, int]
    coeffs: dict[str, list[int]]

    def zeros(
        self: IngredientCoeffs,
        attrib: str,
        val: dict[Ingredient, int],
    ) -> int | float | None:
        """Find zeros for the equation relating to an attribute."""
        if len(other_fixed_set := (set(self.free) - set(val.keys()))) != 1:
            raise ValueError("Need to specify all but one of the free ingredients.")
        other_fixed = other_fixed_set.pop()
        numerator = -self.const[attrib] - sum(
            self.coeffs[attrib][idx] * val[ingred]
            for idx, ingred in enumerate(self.free)
            if ingred != other_fixed
        )
        denominator = self.coeffs[attrib][self.free.index(other_fixed)]
        if denominator:
            if numerator % abs(denominator):
                return numerator / denominator
            else:
                return numerator // denominator
        else:
            return None

    def pos_set(
        self: IngredientCoeffs, attrib: str, val: dict[Ingredient, int]
    ) -> set[int]:
        """Return the set that solve attrib > 0 when all but one ingred is fixed."""
        if len(other_fixed_set := (set(self.free) - set(val.keys()))) != 1:
            raise ValueError("Need to specify all but one of the free ingredients.")
        other_fixed = other_fixed_set.pop()
        zero_point = self.zeros(attrib, val)
        used_already = sum(val.values())
        if zero_point is not None:
            deriv = self.coeffs[attrib][self.free.index(other_fixed)]
            if deriv > 0:
                cutoff = max(0, floor(zero_point + 1))
                return set(range(cutoff, 100 - used_already + 1))
            else:
                cutoff = min(100 - used_already, ceil(zero_point - 1))
                return set(range(0, cutoff + 1))
        else:
            if self.amount(attrib, val | {other_fixed: 0}) > 0:
                return set(range(0, 100 - used_already + 1))
            else:
                return set()

    def calorie_solve(self: IngredientCoeffs, val: dict[Ingredient, int]) -> set[int]:
        """Return the set that solve calories == 500 when all but one ingred is fixed."""
        if len(other_fixed_set := (set(self.free) - set(val.keys()))) != 1:
            raise ValueError("Need to specify all but one of the free ingredients.")
        other_fixed = other_fixed_set.pop()
        numerator = (
            500
            - 100 * self.fixed.calories
            - sum(
                (ingred.calories - self.fixed.calories) * val[ingred]
                for ingred in self.free
                if ingred != other_fixed
            )
        )
        denominator = other_fixed.calories - self.fixed.calories
        if denominator:
            if numerator % abs(denominator):
                return set()
            else:
                return {numerator // denominator}
        else:
            return set()

    def amount(self: IngredientCoeffs, attrib: str, val: dict[Ingredient, int]) -> int:
        """Determine the amount of an attribute based on a recipe."""
        return max(
            self.const[attrib]
            + sum(
                self.coeffs[attrib][self.free.index(key)] * value
                for key, value in val.items()
            ),
            0,
        )

    def total_score(self: IngredientCoeffs, val: dict[Ingredient, int]) -> int:
        """Determine the total score given a mix of ingredients."""
        retval = 1
        for attrib in ATTRIBS:
            retval *= self.amount(attrib, val)
        return retval


class IngredientContext:
    """Respresent puzzle input."""

    def __init__(self: IngredientContext, ingredients: Sequence[Ingredient]) -> None:
        """Initialize object."""
        self.ingredients = list(ingredients)

    @classmethod
    def parse_input(cls: type[IngredientContext], data: str) -> IngredientContext:
        """Parse puzzle input and return a list of ingredients."""
        return cls([Ingredient.from_input(line) for line in data.splitlines()])

    def __repr__(self: IngredientContext) -> str:
        """Return repr(self)."""
        return f"{self.__class__.__name__}({self.ingredients!r})"

    @property
    def coefficients(self: IngredientContext) -> IngredientCoeffs:
        """Return a dictionary of coefficients."""
        fixed = self.ingredients[0]
        free = self.ingredients[1:]

        return IngredientCoeffs(
            fixed,
            free,
            {attrib: 100 * fixed.__getattribute__(attrib) for attrib in ATTRIBS},
            {
                attrib: [
                    k.__getattribute__(attrib) - fixed.__getattribute__(attrib)
                    for k in free
                ]
                for attrib in ATTRIBS
            },
        )


def part1(raw_data: str) -> int:
    """Solve Part 1 of the puzzle."""
    data = IngredientContext.parse_input(raw_data)
    coeffs = data.coefficients
    max_val = 0
    for vals_raw in itertools.product(range(101), repeat=len(coeffs.free) - 1):
        if sum(vals_raw) <= 100:
            vals = {
                ingred: vals_raw[idx] for idx, ingred in enumerate(coeffs.free[:-1])
            }
            possible_vals = set(range(0, 100 - sum(vals_raw) + 1))
            for a in ATTRIBS:
                possible_vals &= coeffs.pos_set(a, vals)
                if len(possible_vals) == 0:
                    break
            if possible_vals:
                for j in possible_vals:
                    max_val = max(
                        max_val, coeffs.total_score(vals | {coeffs.free[-1]: j})
                    )
    return max_val


def part2(raw_data: str) -> int:
    """Solve Part 2 of the puzzle."""
    data = IngredientContext.parse_input(raw_data)
    coeffs = data.coefficients
    max_val = 0
    for vals_raw in itertools.product(range(101), repeat=len(coeffs.free) - 1):
        if sum(vals_raw) <= 100:
            vals = {
                ingred: vals_raw[idx] for idx, ingred in enumerate(coeffs.free[:-1])
            }
            if len(zs := coeffs.calorie_solve(vals)):
                max_val = max(
                    coeffs.total_score(vals | {coeffs.free[-1]: list(zs)[-1]}), max_val
                )
    return max_val


def _test_zero_soln(raw_data: str, print_intermediate: bool = True) -> str:
    data = IngredientContext.parse_input(raw_data)
    coeffs = data.coefficients
    to_pick = len(coeffs.free)
    raw_vals = random.sample(range(80), to_pick - 1)
    vals_list = [b - a for b, a in zip(raw_vals[1:] + [80], [0] + raw_vals[:-1])]
    vals = {ingred: vals_list[idx] for idx, ingred in enumerate(coeffs.free[:-1])}
    a = random.choice(ATTRIBS)
    z = coeffs.zeros(a, vals)
    outstr = f"{coeffs = }\n{vals = }\n{a = }, {z = }"
    if z is not None:
        dict_to_pass = vals | {coeffs.free[-1]: z}
        outstr += f"\n{dict_to_pass = }\n"
        outstr += f"\n{coeffs.amount(a, dict_to_pass) = }"  # type: ignore
    outstr += f"\n{(ps := coeffs.pos_set(a, vals)) = } \n"
    okay = True
    for k in range(0, 101 - sum(vals.values())):
        dict_to_pass2 = vals | {coeffs.free[-1]: k}
        u = coeffs.amount(a, dict_to_pass2)
        if u <= 0:
            if k not in ps:
                outstr += f"[red on black]{k}[/], "
            else:
                outstr += f"[white on red]{k}[/], "
                okay = False
        else:
            if k in ps:
                outstr += f"[green on black]{k}[/], "
            else:
                outstr += f"[white on dark_green]{k}[/], "
                okay = False
    if not print_intermediate:
        outstr = f"{okay}"
    else:
        outstr += f"\n{okay}"
    return outstr


if __name__ == "__main__":
    c = Console()
    if len(argv) == 1:
        c.print(f"[white on red]Usage:[/] [yellow on black]{argv[0]}[/] filename")
    else:
        with open(argv[1], "rt") as infile:
            raw_data = infile.read()
            if len(argv) > 2 and argv[2] == "--test":
                for k in range(20):
                    c.print(_test_zero_soln(raw_data, k < 3))
            else:
                c.print(
                    "[white on dark green]Part 1:[/]"
                    + f" [yellow on black]{part1(raw_data)}[/]"
                )
                c.print(
                    "[white on dark green]Part 2:[/]"
                    + f" [yellow on black]{part2(raw_data)}[/]"
                )
