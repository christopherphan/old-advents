"""Some common code to reuse in these advent puzzle solutions."""

from collections.abc import Callable
from typing import TypeVar

from rich.console import Console

T = TypeVar("T")


def report_results(
    prog_name: str,
    c: Console,
    parse_input: Callable[[str], T],
    result_fcn: dict[str, Callable[[T], str]],
    text: str,
) -> None:
    """Produce and report results using subroutines."""
    program_prefix = f"[green on black]{prog_name}:[/] "
    data = parse_input(text)
    for key, value in result_fcn.items():
        c.print(
            program_prefix
            + f"[cyan on black]{key}[/]: [yellow on black]{value(data)}[/]"
        )


def make_reporter(
    parse_input: Callable[[str], T], result_fcn: dict[str, Callable[[T], str]]
) -> Callable[[Console, str, str], None]:
    """Create a file_fcn that calls the appropriate report_results."""

    def ret_fcn(c: Console, prog_name: str, text: str) -> None:
        report_results(prog_name, c, parse_input, result_fcn, text)

    return ret_fcn


def interactive_loop(
    parse_input: Callable[[str], T],
    result_fcn: dict[str, Callable[[T], str]],
) -> Callable[[Console, str], None]:
    """Implement an interactive loop."""

    def ret_fcn(c: Console, prog_name: str):
        program_prefix = f"[green on black]{prog_name}:[/] "
        while text := c.input(
            program_prefix + "[magenta on black]Input[/] (blank to exit): "
        ):
            try:
                report_results(prog_name, c, parse_input, result_fcn, text)
            except (ValueError, TypeError) as e:
                c.print(program_prefix + f"[white on red]Invalid input[/]: {text}")
                c.print(program_prefix + f"\t{e}")

    return ret_fcn


def print_help(c: Console, prog_name: str) -> None:
    """Print help message for program called without filename."""
    c.print(f"[white on red]Usage:[/] [yellow on black]{prog_name}[/] filename")


def main(
    argv: list[str],
    no_file_fcn: Callable[[Console, str], None],
    file_fcn: Callable[[Console, str, str], None],
) -> None:
    """Run one function if no filename is given, otherwise another."""
    c = Console()
    if len(argv) == 1:
        no_file_fcn(c, argv[0])
    else:
        with open(argv[1], "rt") as infile:
            text = infile.read()
        file_fcn(c, argv[0], text)
