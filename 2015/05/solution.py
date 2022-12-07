"""Solution to day 5 of 2015 Advent of Code."""

import re
from collections.abc import Callable
from sys import argv
from typing import Final

from _resources import Console, interactive_loop, main, report_results

LETTER_BETWEEN: Final[re.Pattern] = re.compile(r"(?P<letter>[a-z])[a-z](?P=letter)")


def is_nice1(x: str) -> bool:
    """Determine if ``x`` is nice (part 1)."""
    return (
        len([k for k in x if k in "aeiou"]) >= 3
        and any(j == k for j, k in zip(x[:-1], x[1:]))
        and all(k not in x for k in ["ab", "cd", "pq", "xy"])
    )


def is_nice2(x: str) -> bool:
    """Determine if ``x`` is nice (Part 2)."""
    return (
        any(x[j : j + 2] in x[j + 2 :] for j in range(len(x) - 2))
    ) and LETTER_BETWEEN.search(x) is not None


INTERACTIVE_RESULTS: Final[dict[str, Callable[[str], str]]] = {
    "Part 1": (lambda x: "Nice" if is_nice1(x) else "Naughty"),
    "Part 2": (lambda x: "Nice" if is_nice2(x) else "Naughty"),
}


def file_fcn(c: Console, prog_name: str, text: str) -> None:
    """Parse file and display results."""
    report_results(
        prog_name,
        c,
        lambda x: x.splitlines(),
        {
            "Part 1": (lambda x: str(sum(is_nice1(k) for k in x))),
            "Part 2": (lambda x: str(sum(is_nice2(k) for k in x))),
        },
        text,
    )


if __name__ == "__main__":
    main(argv, interactive_loop(lambda x: x, INTERACTIVE_RESULTS), file_fcn)
