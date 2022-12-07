"""Some common code to reuse in these advent puzzle solutions."""

from collections.abc import Callable
from typing import TypeVar

from rich.console import Console

T = TypeVar("T")


def report_results(
    c: Console,
    parse_input: Callable[[str], T],
    result_fcn: dict[str, Callable[[T], str]],
    text: str,
) -> None:
    """Produce and report results using subroutines."""
    data = parse_input(text)
    for key, value in result_fcn.items():
        c.print(f"[cyan on black]{key}[/]: [yellow on black]{value(data)}[/]")


def interactive_loop(
    parse_input: Callable[[str], T],
    result_fcn: dict[str, Callable[[T], str]],
) -> Callable[[Console], None]:
    """Implement an interactive loop."""

    def ret_fcn(c: Console):
        while text := c.input("[magenta on black]Input[/] (blank to exit): "):
            try:
                report_results(c, parse_input, result_fcn, text)
            except (ValueError, TypeError) as e:
                c.print(f"[white on red]Invalid input[/]: {text}")
                c.print(f"\t{e}")

    return ret_fcn


def main(
    argv: list[str],
    no_file_fcn: Callable[[Console], None],
    file_fcn: Callable[[str, Console], None],
) -> None:
    """Run one function if no filename is given, otherwise another."""
    c = Console()
    if len(argv) == 1:
        no_file_fcn(c)
    else:
        with open(argv[1], "rt") as infile:
            text = infile.read()
        file_fcn(text, c)
