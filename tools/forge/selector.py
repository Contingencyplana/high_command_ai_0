"""Selector parsing and matching utilities for Forge."""

from __future__ import annotations

import operator
import re
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Protocol


class Record(Protocol):
    def get(self, key: str, default: object | None = None) -> object | None:
        ...


@dataclass(frozen=True)
class Predicate:
    test: Callable[[Record], bool]


_TOKEN_PATTERN = re.compile(r"\s*(AND|OR|>=|<=|!=|=|>|<|:|\(|\))|([^\s()]+)")


def _tokenize(expression: str) -> List[str]:
    tokens: List[str] = []
    for match in _TOKEN_PATTERN.finditer(expression):
        if match.group(1):
            tokens.append(match.group(1))
        elif match.group(2):
            tokens.append(match.group(2))
    return tokens


def _to_postfix(tokens: Iterable[str]) -> List[str]:
    precedence = {"OR": 1, "AND": 2}
    output: List[str] = []
    stack: List[str] = []
    for token in tokens:
        if token in {"AND", "OR"}:
            while stack and stack[-1] != "(" and precedence.get(stack[-1], 0) >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses in selector")
            stack.pop()
        else:
            output.append(token)
    while stack:
        token = stack.pop()
        if token in {"(", ")"}:
            raise ValueError("Mismatched parentheses in selector")
        output.append(token)
    return output


def _compare(op: Callable[[float, float], bool]) -> Callable[[object, object], bool]:
    def inner(lhs: object, rhs: object) -> bool:
        try:
            return op(float(lhs), float(rhs))
        except (TypeError, ValueError):
            return False

    return inner


_COMPARATORS: Dict[str, Callable[[object, object], bool]] = {
    ":": lambda actual, expected: str(actual) == str(expected),
    "=": lambda actual, expected: str(actual) == str(expected),
    "!=": lambda actual, expected: str(actual) != str(expected),
    ">": _compare(operator.gt),
    ">=": _compare(operator.ge),
    "<": _compare(operator.lt),
    "<=": _compare(operator.le),
}


def _make_predicate(token: str) -> Predicate:
    match = re.match(r"(?P<field>[A-Za-z0-9_.-]+)(?P<op>:|=|!=|>=|<=|>|<)(?P<value>.+)", token)
    if not match:
        raise ValueError(f"Invalid selector token '{token}'")
    field = match.group("field")
    op_symbol = match.group("op")
    value = match.group("value")
    comparator = _COMPARATORS.get(op_symbol)
    if comparator is None:
        raise ValueError(f"Unsupported comparator '{op_symbol}' in selector")

    def test(record: Record) -> bool:
        actual = record.get(field)
        return comparator(actual, value)

    return Predicate(test=test)


def build_predicate(expression: str) -> Predicate:
    if not expression:
        return Predicate(test=lambda record: True)
    tokens = _tokenize(expression)
    postfix = _to_postfix(tokens)
    stack: List[Predicate] = []
    for token in postfix:
        if token == "AND":
            right = stack.pop()
            left = stack.pop()
            stack.append(Predicate(test=lambda record, left_pred=left, right_pred=right: left_pred.test(record) and right_pred.test(record)))
        elif token == "OR":
            right = stack.pop()
            left = stack.pop()
            stack.append(Predicate(test=lambda record, left_pred=left, right_pred=right: left_pred.test(record) or right_pred.test(record)))
        else:
            stack.append(_make_predicate(token))
    if len(stack) != 1:
        raise ValueError("Invalid selector expression")
    return stack[0]


def filter_records(records: Iterable[Record], expression: str) -> List[Record]:
    predicate = build_predicate(expression)
    return [record for record in records if predicate.test(record)]
