from __future__ import annotations

from contango.trading.execution.engine.fills.fill_policy import FillPolicy
from contango.trading.execution.engine.fills.fill_rule import FillRule


class _AlwaysPassRule(FillRule[int]):
    @property
    def reason(self) -> str:
        return "always pass"

    def validate(self, context: int) -> bool:
        return True


class _AlwaysFailRule(FillRule[int]):
    def __init__(self, reason: str) -> None:
        self._reason = reason

    @property
    def reason(self) -> str:
        return self._reason

    def validate(self, context: int) -> bool:
        return False


def test_returns_none_when_all_rules_pass() -> None:
    policy = FillPolicy[int]((_AlwaysPassRule(), _AlwaysPassRule()))

    assert policy.validate_rules(0) is None


def test_returns_none_when_there_are_no_rules() -> None:
    policy = FillPolicy[int](())

    assert policy.validate_rules(0) is None


def test_returns_the_reason_of_the_first_failing_rule() -> None:
    policy = FillPolicy[int]((
        _AlwaysPassRule(),
        _AlwaysFailRule("first failure"),
        _AlwaysFailRule("second failure"),
    ))

    assert policy.validate_rules(0) == "first failure"


def test_does_not_evaluate_rules_after_the_first_failure() -> None:
    evaluated: list[str] = []

    class _RecordingFailRule(FillRule[int]):
        def __init__(self, name: str) -> None:
            self._name = name

        @property
        def reason(self) -> str:
            return self._name

        def validate(self, context: int) -> bool:
            evaluated.append(self._name)
            return False

    policy = FillPolicy[int]((_RecordingFailRule("a"), _RecordingFailRule("b")))
    policy.validate_rules(0)

    assert evaluated == ["a"]
