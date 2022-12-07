"""Solution to day 4 of 2015 Advent of Code."""

from hashlib import md5
from sys import argv

from _resources import Console, interactive_loop, main, report_results


def hash(x: str) -> str:
    """Hash a string using MD5."""
    return md5(x.encode(), usedforsecurity=False).hexdigest()


def find_soln(key: str, num_zeros: int = 5) -> str:
    """Find the lowest ``k`` such that ``hash(f"{key}{k}")`` begins with specified zeros."""
    k: int = 1
    while hash(f"{key}{k}")[:num_zeros] != "0" * num_zeros:
        k += 1
    return str(k)


parts = {"Part 1": (lambda x: find_soln(x, 5)), "Part 2": (lambda x: find_soln(x, 6))}


def file_func(c: Console, prog_name: str, data: str) -> None:
    """Report output from data in file."""
    report_results(prog_name, c, lambda x: x, parts, data)


if __name__ == "__main__":
    main(argv, interactive_loop(lambda x: x, parts), file_func)
