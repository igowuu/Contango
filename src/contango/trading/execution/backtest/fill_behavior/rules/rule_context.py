from __future__ import annotations

from typing import NamedTuple


class RuleContext(NamedTuple):
    """
    The context for all rules.
    
    Attributes:
        desired_quantity: The desired quantity of units for the order.
        current_position: The current position in units for the order.
        total_cost: The total cost for the order.
        current_cash: The current cash available in the portfolio.
    """
    desired_quantity: int
    current_position: int
    total_cost: float
    current_cash: float
