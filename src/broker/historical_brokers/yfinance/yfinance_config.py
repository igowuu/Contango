# broker/historical_brokers/yfinance/yfinance_config.py — part of Contango, a parameterized backtesting & execution framework
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

from dataclasses import dataclass

from broker.historical_brokers.config_type import Config


@dataclass
class YfinanceConfig(Config):
    """
    Holds the configuration for deriving data from the yfinance broker.
    
    Attributes:
        ticker: The ticker symbol (e.g. AAPL) to derive yfinance data from.
        start_date: The start date (YYYY-MM-DD) to derive yfinance data from.
        end_date: The end date (YYYY-MM-DD) to derive yfinance data from.
        interval: The trading interval to derive yfinance data from.
    """
    pass
