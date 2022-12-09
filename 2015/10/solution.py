"""Solution to day 10 of advent of code."""

from typing import Any


def look_say(x: Any) -> str:
    """Implement Conway's look-say sequences."""
    outstr = ""
    s = str(x)
    cur_val = s[0]
    cur_count = 1
    for k in s[1:]:
        if k != cur_val:
            outstr += f"{cur_count}{cur_val}"
            cur_val = k
            cur_count = 1
        else:
            cur_count += 1
    return outstr + f"{cur_count}{cur_val}"


def repeated_look_say(x: Any, num: int, print_output: bool = False) -> str:
    """Apply the look_say function num times to x."""
    s = str(x)
    for _ in range(num):
        s = look_say(s)
        if print_output:
            print(s)
    return s


if __name__ == "__main__":
    x = input("Enter input: ")
    part1_lss = repeated_look_say(x, 40)
    print(f"Part 1: {len(part1_lss)}")
    print(f"Part 2: {len(repeated_look_say(part1_lss, 10))}")
