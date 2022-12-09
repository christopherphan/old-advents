"""Solution to day 11 of 2015 Advent of Code."""
import re
import string
from collections.abc import Callable
from typing import Final

conditions: list[Callable[[str], bool]] = []

PAIR: Final[re.Pattern] = re.compile(r"(?P<let>[a-z])(?P=let)")


def increment(x: str) -> str:
    """Increment the password by 1 letter."""
    if any(k not in string.ascii_lowercase for k in x):
        raise ValueError("Input must be all lowercase ASCII letters.")
    if len(x) == 0:
        return "a"
    if x[-1] == "z":
        return increment(x[:-1]) + "a"
    else:
        return x[:-1] + chr(ord(x[-1]) + 1)


def register(
    cond_list: list[Callable[[str], bool]]
) -> Callable[[Callable[[str], bool]], Callable[[str], bool]]:
    """Return a decorator to add condition functions to a condition list."""

    def decorator(f: Callable[[str], bool]) -> Callable[[str], bool]:
        """Add f to the list of conditions."""
        cond_list.append(f)
        return f

    return decorator


def check_conds(x: str, cond_list: list[Callable[[str], bool]]) -> bool:
    """Check that x meets all the conditions."""
    return all(f(x) for f in cond_list)


def next_password(
    pwd: str, cond_list: list[Callable[[str], bool]], output: bool = False
) -> str:
    """Return the next acceptable password."""
    new_pwd = increment(pwd)
    while not check_conds(new_pwd, cond_list):
        new_pwd = increment(new_pwd)
    if output:
        print(f"{pwd}: {new_pwd}")
    return new_pwd


@register(conditions)
def has_straight(x: str) -> bool:
    """Check if the password has an increasing straight."""
    return any(
        (
            x[j + 1] == increment(x[j])
            and x[j + 2] == increment(x[j + 1])
            and x[j] not in "yz"
        )
        for j in range(len(x) - 3)
    )


@register(conditions)
def no_bad_letters(x: str) -> bool:
    """Check that the password is devoid of i, o, or l."""
    return all(k not in x for k in "iol")


@register(conditions)
def has_pairs(x: str) -> bool:
    """Check that the password has distinct non-overlapping pairs of letters."""
    return len(set(PAIR.findall(x))) >= 2


if __name__ == "__main__":
    for k in ["abcdefgh", "ghijklmn"]:
        next_password(k, conditions, True)

    pwd = "vzbxkghb"
    for _ in range(2):
        pwd = next_password(pwd, conditions, True)
