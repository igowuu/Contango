# trading/execution/engine/events/event_bus.py — part of Contango, a parameterized backtesting & execution framework
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

from collections import defaultdict
from typing import Any, Callable


_handler_type = Callable[[Any], None]


class EventBus:
    """
    Allows for methods to subscribe whenever a specific event is published.
    """
    def __init__(self) -> None:
        """
        Initializes `EventBus` with empty subscriptions.
        """
        self._handlers: dict[type, list[_handler_type]] = defaultdict(list)
        self._priorities: dict[type, list[int]] = defaultdict(list)

    def subscribe(
        self,
        event_type: type,
        handler: _handler_type,
        priority: int,
    ) -> None:
        """
        Subscribes a handler to an event type. Higher priority handlers execute first.

        Args:
            event_type: The type for the event to be subscribed to.
            handler: The method that recieves the event.
            priority: The priority (highest first) for the subscription.
        """
        if priority in self._priorities[event_type]:
            raise ValueError("Two subscriptions must not have the same priority!")

        self._priorities[event_type].append(priority)
        self._handlers[event_type].append(handler)
        
        # Sort both lists together by priority descending
        paired = sorted(
            zip(self._priorities[event_type], self._handlers[event_type]),
            reverse=True
        )
        self._priorities[event_type] = [p for p, _ in paired]
        self._handlers[event_type] = [h for _, h in paired]

    def publish(self, event: object) -> None:
        """
        Publishes an event to all handlers registered for its type.

        Args:
            event: The underlying event to publish.
        """
        handlers = self._handlers.get(type(event))

        if handlers is None:
            return

        for handler in handlers:
            handler(event)
