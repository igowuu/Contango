from __future__ import annotations

from typing import TypeVar, Generic
from abc import ABC, abstractmethod

from contango.strategy.rule_based.contexts.context import Context


C = TypeVar("C", bound=Context)


class Condition(ABC, Generic[C]):
    """
    A single condition when creating a strategy.
    """
    @abstractmethod
    def evaluate(self, context: C) -> bool:
        """
        Returns the status of a condition given a context object.
        """
        ...

    def __and__(self, other: "Condition[C]") -> Condition[C]:
        return And(self, other)

    def __or__(self, other: "Condition[C]") -> Condition[C]:
        return Or(self, other)

    def __invert__(self) -> Condition[C]:
        return Not(self)


class And(Condition[C]):
    def __init__(self, first: Condition[C], second: Condition[C]) -> None:
        self._first = first
        self._second = second

    def evaluate(self, context: C) -> bool:
        return self._first.evaluate(context) and self._second.evaluate(context)

    def __str__(self) -> str:
        return f"{self._first} & {self._second}"


class Or(Condition[C]):
    def __init__(self, first: Condition[C], second: Condition[C]) -> None:
        self._first = first
        self._second = second

    def evaluate(self, context: C) -> bool:
        return self._first.evaluate(context) or self._second.evaluate(context)

    def __str__(self) -> str:
        return f"{self._first} | {self._second}"


class Not(Condition[C]):
    def __init__(self, condition: Condition[C]) -> None:
        self._condition = condition

    def evaluate(self, context: C) -> bool:
        return not self._condition.evaluate(context)

    def __str__(self) -> str:
        return f"!{self._condition}"
