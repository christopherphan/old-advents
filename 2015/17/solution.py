"""Solution to Day 17 of 2015 Advent of Code."""

from collections import Counter
from collections.abc import Sequence, Set
from sys import argv
from typing import Final

from rich.console import Console


def _amount_held(all_containers: Sequence[int], selected: Set[int]) -> int:
    """Return the amount held by selected containers."""
    return sum(all_containers[idx] for idx in selected)


def possible_combos(
    all_containers: Sequence[int], selected: Set[int], total_nog: int
) -> Counter:
    """
    Return the number of possible container combinations that include those in selected.

    The parameter ``selected`` is given as a set of INDICIES of all_containers.
    """
    if (ah := _amount_held(all_containers, selected)) > total_nog:
        return Counter()
    elif ah == total_nog:
        return Counter({len(selected)})
    else:
        # We have to be careful not to overcount. We can avoid this by only adding
        # containers with indicies bigger than those in selected.
        return sum(
            [
                possible_combos(all_containers, selected | {k}, total_nog)
                for k in range(
                    (max(selected) if selected else -1) + 1, len(all_containers)
                )
            ],
            start=Counter(),
        )


def parse_input(text: str) -> list[int]:
    """Parse the puzzle input."""
    return [int(k.strip()) for k in text.splitlines()]


if __name__ == "__main__":
    c = Console()
    if len(argv) < 3:
        c.print(
            f"[white on red]Usage:[/] [yellow on black]{argv[0]}[/]"
            + " [i]filename[/] [i]amt_to_store[/]"
        )
    else:
        with open(argv[1], "rt") as infile:
            data = infile.read()
        total_nog = int(argv[2])
        containers = parse_input(data)
        pc = possible_combos(containers, set(), total_nog)
        c.print(
            "[white on dark_green]Part 1:[/]" + f" [yellow on black]{pc.total()}[/]"
        )
        c.print(
            "[white on dark_blue]Part 2:[/] "
            + f"[yellow on black]{pc[min(pc.keys())]}[/]"
        )
