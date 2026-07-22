# tests/unit/trading/test_execution/test_engine/test_event_bus.py — part of Contango, a parameterized backtesting & execution framework
# Copyright (C) 2026  Jacob Taylor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

import pytest

from trading.execution.engine.events.event_bus import EventBus


class EventA:
    def __init__(self, payload: str = "") -> None:
        self.payload = payload


class EventB:
    def __init__(self, payload: str = "") -> None:
        self.payload = payload


@pytest.fixture
def bus() -> EventBus:
    return EventBus()


def test_publish_calls_subscribed_handler(bus: EventBus) -> None:
    received: list[EventA] = []
    bus.subscribe(EventA, received.append, priority=0)

    event = EventA("hello")
    bus.publish(event)

    assert received == [event]


def test_publish_with_no_subscribers_does_not_raise(bus: EventBus) -> None:
    bus.publish(EventA("hello"))


def test_publish_only_calls_handlers_for_matching_event_type(bus: EventBus) -> None:
    a_received: list[EventA] = []
    b_received: list[EventB] = []
    bus.subscribe(EventA, a_received.append, priority=0)
    bus.subscribe(EventB, b_received.append, priority=0)

    event_a = EventA()
    bus.publish(event_a)

    assert a_received == [event_a]
    assert b_received == []


def test_multiple_events_of_same_type_each_trigger_handler(bus: EventBus) -> None:
    received: list[EventA] = []
    bus.subscribe(EventA, received.append, priority=0)

    e1, e2, e3 = EventA("1"), EventA("2"), EventA("3")
    bus.publish(e1)
    bus.publish(e2)
    bus.publish(e3)

    assert received == [e1, e2, e3]


def test_handlers_execute_in_descending_priority_order(bus: EventBus) -> None:
    call_order: list[str] = []
    bus.subscribe(EventA, lambda e: call_order.append("low"), priority=0)
    bus.subscribe(EventA, lambda e: call_order.append("high"), priority=10)
    bus.subscribe(EventA, lambda e: call_order.append("mid"), priority=5)

    bus.publish(EventA())

    assert call_order == ["high", "mid", "low"]


def test_priority_order_holds_regardless_of_subscription_order(bus: EventBus) -> None:
    call_order: list[str] = []
    bus.subscribe(EventA, lambda e: call_order.append("mid"), priority=5)
    bus.subscribe(EventA, lambda e: call_order.append("high"), priority=10)
    bus.subscribe(EventA, lambda e: call_order.append("low"), priority=0)

    bus.publish(EventA())

    assert call_order == ["high", "mid", "low"]


def test_negative_priorities_are_supported(bus: EventBus) -> None:
    call_order: list[str] = []
    bus.subscribe(EventA, lambda e: call_order.append("neg"), priority=-5)
    bus.subscribe(EventA, lambda e: call_order.append("zero"), priority=0)
    bus.subscribe(EventA, lambda e: call_order.append("pos"), priority=5)

    bus.publish(EventA())

    assert call_order == ["pos", "zero", "neg"]


def test_priority_ordering_is_independent_per_event_type(bus: EventBus) -> None:
    call_order: list[str] = []
    bus.subscribe(EventA, lambda e: call_order.append("a_low"), priority=0)
    bus.subscribe(EventA, lambda e: call_order.append("a_high"), priority=10)
    bus.subscribe(EventB, lambda e: call_order.append("b_high"), priority=1)
    bus.subscribe(EventB, lambda e: call_order.append("b_low"), priority=0)

    bus.publish(EventA())
    bus.publish(EventB())

    assert call_order == ["a_high", "a_low", "b_high", "b_low"]


def test_duplicate_priority_for_same_event_type_raises(bus: EventBus) -> None:
    bus.subscribe(EventA, lambda e: None, priority=1)

    with pytest.raises(ValueError):
        bus.subscribe(EventA, lambda e: None, priority=1)


def test_same_priority_allowed_across_different_event_types(bus: EventBus) -> None:
    bus.subscribe(EventA, lambda e: None, priority=1)
    bus.subscribe(EventB, lambda e: None, priority=1)


def test_failed_subscribe_does_not_corrupt_existing_subscriptions(bus: EventBus) -> None:
    call_order: list[str] = []
    bus.subscribe(EventA, lambda e: call_order.append("first"), priority=1)

    with pytest.raises(ValueError):
        bus.subscribe(EventA, lambda e: call_order.append("second"), priority=1)

    bus.publish(EventA())

    assert call_order == ["first"]


def test_multiple_handlers_all_receive_same_event_instance(bus: EventBus) -> None:
    received_by_1: list[EventA] = []
    received_by_2: list[EventA] = []
    bus.subscribe(EventA, received_by_1.append, priority=1)
    bus.subscribe(EventA, received_by_2.append, priority=0)

    event = EventA("shared")
    bus.publish(event)

    assert received_by_1 == [event]
    assert received_by_2 == [event]


def test_handler_can_mutate_shared_state_in_priority_order(bus: EventBus) -> None:
    def uppercase_handler(e: EventA) -> None:
        e.payload = e.payload.upper()

    def append_handler(e: EventA) -> None:
        e.payload += "!"

    bus.subscribe(EventA, uppercase_handler, priority=10)
    bus.subscribe(EventA, append_handler, priority=0)

    event = EventA("hello")
    bus.publish(event)

    assert event.payload == "HELLO!"
