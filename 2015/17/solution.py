"""Solution to Day 17 of 2015 Advent of Code."""

from collections.abc import Sequence, Set
from sys import argv
from typing import Final

from rich.console import Console


def _amount_held(all_containers: Sequence[int], selected: Set[int]) -> int:
    """Return the amount held by selected containers."""
    return sum(all_containers[idx] for idx in selected)


def possible_combos(
    all_containers: Sequence[int], _selected: Set[int], total_nog: int
) -> dict[int, frozenset[frozenset[int]]]:
    """
    Return the number of possible container combinations that include those in selected.

    The parameter ``selected`` is given as a set of INDICIES of all_containers.
    """
    selected = frozenset(_selected)
    if (ah := _amount_held(all_containers, selected)) > total_nog:
        return dict()
    elif ah == total_nog:
        return {len(selected): frozenset([selected])}
    else:
        # We have to be careful not to overcount. We can avoid this by only adding
        # containers with indicies bigger than those in selected.
        ret_dict: dict[int, frozenset[frozenset[int]]] = {
            u + 1: frozenset() for u, _ in enumerate(all_containers)
        }
        for k in range((max(selected) if selected else -1) + 1, len(all_containers)):
            for key, value in possible_combos(
                all_containers, frozenset(list(selected) + [k]), total_nog
            ).items():
                ret_dict[key] |= value
        return ret_dict


def parse_input(text: str) -> list[int]:
    """Parse the puzzle input."""
    return [int(k.strip()) for k in text.splitlines()]


def _fs_color(x: frozenset) -> str:
    return (
        "[magenta]{[/]"
        + "[magenta],[/]".join(f"[cyan]{k}[/]" for k in x)
        + "[magenta]}[/]"
    )


if __name__ == "__main__":
    c = Console()
    if len(argv) < 3:
        c.print(
            f"[white on red]Usage:[/] [yellow on black]{argv[0]}[/]"
            + " [i]filename[/] [i]amt_to_store[/] [--verbose]"
        )
    else:
        with open(argv[1], "rt") as infile:
            data = infile.read()
        total_nog = int(argv[2])
        containers = parse_input(data)
        pc = possible_combos(containers, set(), total_nog)
        total = sum(len(value) for value in pc.values())
        c.print("[white on dark_green]Part 1:[/]" + f" [yellow on black]{total}[/]")
        keys_with_solns = [k for k in pc.keys() if pc[k]]
        best_num_conts = min(keys_with_solns) if total else None
        if best_num_conts is not None:
            min_container_combos = len(pc[best_num_conts])
        else:
            min_container_combos = 0
        c.print(
            "[white on dark_blue]Part 2:[/] "
            + f"[yellow on black]{min_container_combos}[/]"
        )
        if len(argv) == 4 and argv[3] == "--verbose":
            c.print(
                "[white on blue]Containers:[/] "
                + ", ".join(
                    f"[cyan on black]#{idx}[/] ([green on black]{item}[/])"
                    for idx, item in enumerate(containers)
                )
            )
            for key, value in pc.items():
                if value:
                    c.print(
                        f"[white on dark_green]{key} containers[/]"
                        + f" ([yellow on black]{len(value)}[/]): "
                        + ", ".join(_fs_color(k) for k in value)
                    )
