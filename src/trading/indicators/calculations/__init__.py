# trading/indicators/calculations/__init__.py — part of Contango, a parameterized backtesting & execution framework
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

from trading.indicators.calculations.average_true_range import AverageTrueRange
from trading.indicators.calculations.bollinger_bands import BollingerBands, BollingerBandSnapshot
from trading.indicators.calculations.ema import EMA
from trading.indicators.calculations.rsi import RSI
from trading.indicators.calculations.sma import SMA
from trading.indicators.calculations.true_range import TrueRange
from trading.indicators.calculations.vwap import VWAP, VWAPSnapshot
from trading.indicators.calculations.wilder_average import WilderAverage


__all__ = [
    'AverageTrueRange', 'BollingerBands', 'BollingerBandSnapshot',
    'EMA', 'RSI', 'SMA', 'TrueRange', 'VWAP', 'VWAPSnapshot', 'WilderAverage'
]
