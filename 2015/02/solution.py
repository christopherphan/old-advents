"""Solution to Day 2 of 2015 Advent of Code."""

from sys import argv

from rich.console import Console


def parse_input(text: str) -> tuple[int, int, int]:
    """Parse a line of the input."""
    return tuple(int(k.strip()) for k in text.split("x", maxsplit=2))


def paper_needed(length: int, width: int, height: int) -> int:
    """Determine how much paper is needed."""
    side_areas = [length * width, width * height, height * length]
    return sum([2 * k for k in side_areas]) + min(side_areas)


def ribbon_needed(length: int, width: int, height: int) -> int:
    """Determine how much ribbon is needed."""
    face_perimeters = [2 * k for k in [length + width, length + height, width + height]]
    return length * width * height + min(face_perimeters)


def give_part1_result(paper: int, c: Console, total: bool = False) -> None:
    """Report the result for Part 1."""
    c.print(f"{'Total p' if total else 'P'}aper needed: [yellow on black]{paper} ft^2")


def give_part2_result(ribbon: int, c: Console, total: bool = False) -> None:
    """Report the result for Part 2."""
    c.print(f"{'Total r' if total else 'R'}ibbon needed: [yellow on black]{ribbon} ft")


def interactive_loop(c: Console) -> None:
    """Implement the interactive loop."""
    while text := c.input("[magenta on black]Input[/] (blank to exit): "):
        try:
            dimensions = parse_input(text)
            paper = paper_needed(*dimensions)
            give_part1_result(paper, c)
            ribbon = ribbon_needed(*dimensions)
            give_part2_result(ribbon, c)
        except (ValueError, TypeError) as e:
            c.print(f"[white on red]Invalid input[/]: {text}")
            c.print(f"\t{e}")


if __name__ == "__main__":
    c = Console()
    if len(argv) == 1:
        interactive_loop(c)
    else:
        with open(argv[1], "rt") as infile:
            text = infile.read()
        dimensions = [
            parse_input(pros_line)
            for line in text.splitlines()
            if (pros_line := line.strip())
        ]
        total_paper = sum(paper_needed(*k) for k in dimensions)
        give_part1_result(total_paper, c, True)
        total_ribbon = sum(ribbon_needed(*k) for k in dimensions)
        give_part2_result(total_ribbon, c, True)
