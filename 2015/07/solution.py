"""Solution to Day 7 of 2015 Advent of Code."""
from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from sys import argv
from typing import Final

from _resources import Console, main, make_reporter, print_help

EXPR_PARSER: Final[re.Pattern] = re.compile(
    r"((?P<val1>[a-z]+|\d+) )?((?P<op>[A-Z]+) )?(?P<val2>[a-z]+|\d+)"
)


@dataclass
class AssignmentExpression:
    """Represent the LHS of a line of puzzle input."""

    val1: str | int | None
    val2: str | int
    op: str | None

    @classmethod
    def from_text(cls: type[AssignmentExpression], expr: str) -> AssignmentExpression:
        """Parse the LHS of a line of puzze input."""
        if not (m := EXPR_PARSER.match(expr)):
            raise ValueError(f"Bad expression: {expr}")
        val1 = m.group("val1")
        val2 = m.group("val2")
        if val1 is not None and val1.isdigit():
            val1 = int(val1)
        if val2.isdigit():
            val2 = int(val2)
        return cls(val1, val2, m.group("op"))

    @property
    def simple(self: AssignmentExpression) -> bool:
        """Return True if the expression is equivalent to an integer."""
        return self.val1 is None and self.op is None and isinstance(self.val2, int)

    @property
    def parents(self: AssignmentExpression) -> list[str]:
        """Return a list of variables referenced in the expression."""
        return [k for k in [self.val1, self.val2] if isinstance(k, str)]

    def simplify(self: AssignmentExpression, eval_state: EvaluationState) -> int:
        """Simplify the expression and return the value."""
        if self.simple:
            assert isinstance(self.val2, int)
            return self.val2
        if self.val1 is None and (self.op is not None and self.op != "NOT"):
            raise ValueError(f"Missing operand for {self.op}")
        elif self.val1 is None:
            if isinstance(self.val2, str):
                val = eval_state.state[self.val2].simplify(eval_state)
                if self.op is None:
                    self.val2 = val
                elif self.op == "NOT":
                    self.val2 = ~val & 65535
                    self.op = None
            else:  # self.op == "NOT"
                self.val2 = ~self.val2 & 65535
                self.op = None
            assert isinstance(self.val2, int)
            return self.val2
        val1: int
        if isinstance(self.val1, str):
            val1 = eval_state.state[self.val1].simplify(eval_state)
        elif self.val1 is not None:
            val1 = self.val1
        else:
            val1 = 0
        self.val1 = None
        if isinstance(self.val2, str):
            val2 = eval_state.state[self.val2].simplify(eval_state)
        else:
            val2 = self.val2
        if self.op == "LSHIFT":
            self.val2 = val1 << val2
        elif self.op == "RSHIFT":
            self.val2 = val1 >> val2
        elif self.op == "AND":
            self.val2 = val1 & val2
        elif self.op == "OR":
            self.val2 = val1 | val1
        assert isinstance(self.val2, int)
        self.op = None
        self.val2 = self.val2 & 65535
        return self.val2


@dataclass
class ExpandState:
    """Keep track of which variables have been expanded in the eval stack."""

    varname: str
    expanded: bool


@dataclass
class EvaluationState:
    """Represent an intermediate evaluation of the variables."""

    state: dict[str, AssignmentExpression]

    def evaluate(self: EvaluationState, var: str) -> int:
        """Evaluate the variable, simplifying the state as we go along."""
        if var not in self.state:
            raise NameError(f"{var} is not evaluation state.")
        eval_stack: list[ExpandState] = [
            ExpandState(var, bool(self.state[var].parents))
        ]
        while unexpanded := [k for k in eval_stack if not k.expanded]:
            for k in unexpanded:
                for p in self.state[k.varname].parents:
                    eval_stack.append(ExpandState(p, bool(self.state[p].parents)))

        while eval_stack:
            self.state[eval_stack.pop().varname].simplify(self)

        return self.state[var].simplify(self)


@dataclass
class AssignmentStatement:
    """Represent an assignment statement."""

    target: str
    expr: AssignmentExpression

    @classmethod
    def from_text(cls: type[AssignmentStatement], text: str) -> AssignmentStatement:
        """Parse a line of the puzzle input."""
        expr, target = text.split(" -> ", maxsplit=1)
        return cls(target, AssignmentExpression.from_text(expr))

    def add_to(self: AssignmentStatement, eval_state: EvaluationState) -> None:
        """Add the assignment expression to ``var_dict``."""
        eval_state.state[self.target] = self.expr


def parse_input(data: str) -> EvaluationState:
    """Parse the input and set up an evaluation state."""
    eval_state = EvaluationState({})
    for line in data.splitlines():
        AssignmentStatement.from_text(line).add_to(eval_state)
    return eval_state


RESULT_FCNS: Final[dict[str, Callable[[EvaluationState], str]]] = {
    "Part 1": (lambda eval_state: str(eval_state.evaluate("a")))
}

if __name__ == "__main__":
    main(argv, print_help, make_reporter(parse_input, RESULT_FCNS))
