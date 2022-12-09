"""Solution to Day 8 of 2015 Advent of Code."""

from sys import argv

from _resources import main, make_reporter, print_help


def extra_chars(text: str) -> int:
    """Return the number of extra characters in the literal compared to in memory."""
    text = text[1:-1]  # Get rid of delimiting quotation marks
    chars_left = len(text)
    extra = 2  # The quotation marks at the start/end count as 2
    skip = 0
    for idx, char in enumerate(text):
        chars_left -= 1
        if skip == 0 and char == "\\":
            if (
                chars_left >= 3
                and text[idx + 1] == "x"
                and all(k in "1234567890abcdefABCDEF" for k in text[idx + 2 : idx + 4])
                # hex digits
            ):
                extra += 3
                skip = 3
            elif chars_left > 0 and text[idx + 1] in ["\\", '"']:
                extra += 1
                skip = 1
        else:
            skip = max(0, skip - 1)
    return extra


if __name__ == "__main__":
    main(
        argv,
        print_help,
        make_reporter(
            lambda x: x.splitlines(),
            {"Part 1": (lambda x: str(sum(extra_chars(k) for k in x)))},
        ),
    )
