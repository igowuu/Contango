# Indicator Calculations

Indicators are generally used for statistical analysis (using OHLCV data to determine when to trade). Although this list will not go into depth on what each indicator means, it will briefly mention some of the indicators available in the codebase:

- **Average True Range (ATR):** Measures market volatility by averaging the true range (largest of the current high-low range, or gaps from the prior close) over a set period.
- **Bollinger Bands:** Plots bands above and below a moving average based on standard deviation, used to gauge volatility and potential overbought/oversold conditions.
- **Exponential Moving Average (EMA):** A moving average that weights recent prices more heavily, making it more responsive to new price changes than a simple average.
- **Relative Strength Index (RSI):** A momentum oscillator that measures the speed and magnitude of recent price changes to identify overbought or oversold conditions.
- **Simple Moving Average (SMA):** The unweighted average of a security's price over a specified number of periods.
- **True Range:** The greatest of the current high minus low, current high minus previous close, or current low minus previous close, used as the basis for volatility measures like ATR.
- **Volume Weighted Average Price (VWAP):** The average price of a security weighted by trading volume over a given period, often used as a benchmark for trade execution quality.
- **Wilder Average:** A smoothing technique (developed by J. Welles Wilder) that applies more weight to recent data while retaining a longer memory of past values, used as the basis for indicators like ATR and RSI.

# Indicator State

Often, strategies use indicator states (price below or above an indicator) rather than looking for specific values. State machines for each of the indicators are included. For example:

**EMA** -> States ABOVE and BELOW
**Bollinger Bands** -> States BELOW_LOWER, BETWEEN_LOWER_AND_MIDDLE, BETWEEN_MIDDLE_AND_HIGHER, and ABOVE_HIGHER.
