"""Some common code to reuse in these advent puzzle solutions."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from rich.console import Console


@dataclass
class PuzzleSolution:
    """Represent a solution to the puzzle."""

    input_parser: Callable[[str], dict]
    result_fcns: dict[str, Callable[[dict], str]]
    puzzle_inputs: dict[str, str]

    @classmethod
    def from_parser(
        cls: type[PuzzleSolution], input_parser: Callable[[str], dict]
    ) -> PuzzleSolution:
        """Create a PuzzleSolution class from a input_parser function."""
        return cls(input_parser, dict(), dict())

    def register_result_function(
        self: PuzzleSolution, result_name: str
    ) -> Callable[[Callable[[dict], str]], Callable[[dict], str]]:
        """Create a decorator to place a function in the result_fcns dict."""

        def decorator(result_fcn: Callable[[dict], str]) -> Callable[[dict], str]:
            """Register the function as the {} solution."""
            self.result_fcns[result_name] = result_fcn
            return result_fcn

        assert decorator.__doc__ is not None
        decorator.__doc__ = decorator.__doc__.format(result_name)
        return decorator

    def add_input(self: PuzzleSolution, filename: str, name: str) -> None:
        """Add the contents of a file to the puzzle input dictionary."""
        with open(filename, "rt") as infile:
            self.puzzle_inputs[name] = infile.read()

    def report_results(
        self: PuzzleSolution,
        c: Console,
        prog_name: str,
    ) -> None:
        """Produce and report results using subroutines."""
        program_prefix = f"[green on black]{prog_name}:[/] "
        for key_input, text in self.puzzle_inputs.items():
            input_prefix = f"[light_green on black]{key_input}:[/] "
            data = self.input_parser(text)
            for result_key, fcn in self.result_fcns.items():
                c.print(
                    program_prefix
                    + input_prefix
                    + f"[cyan on black]{result_key}[/]: [yellow on black]{fcn(data)}[/]"
                )


def main_files(argv: list[str], pz: PuzzleSolution, default_files: list[str]):
    """Implement main program action when files are specified."""
    c = Console()
    if len(argv) == 1:
        for filename in default_files:
            pz.add_input(filename, filename)
    else:
        for k in argv[1:]:
            pz.add_input(k, k)

    pz.report_results(c, argv[0])
