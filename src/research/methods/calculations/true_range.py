from __future__ import annotations


USD = float


class TrueRange:
    """
    The volatility during a single trading period.
    """
    def __init__(self) -> None:
        """
        Initializes `TrueRange`.
        """
        self._previous_close: USD | None = None

    def update(self, high: USD, low: USD, close: USD) -> float:
        """
        Updates the state of the true range for every bar.
        
        Args:
            high: The highest price reached in USD for a bar.
            low: The lowest price reached in USD for a bar.
            close: The closing price in USD for a bar.
        
        Returns:
            float: The true range for the bar.
        """
        if self._previous_close is None:
            tr = high - low
        else:
            tr = max(
                high - low,
                abs(high - self._previous_close),
                abs(low - self._previous_close),
            )

        self._previous_close = close
        return tr