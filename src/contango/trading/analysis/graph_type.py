from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, final

import pandas as pd
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]

from contango.trading.analysis.graph_config import GraphConfig


C = TypeVar("C", bound=GraphConfig)


class GraphType(ABC, Generic[C]):
    """
    A generic abstract class that all graphs should implement.
    
    Attributes:
        C: The `GraphConfig` for the class.

        graph_name: The unique name for the graph.
    """
    graph_name: str

    def __init__(self, config: C) -> None:
        """
        Initializes `GraphType`.
        
        Args:
            config: The matching configuration for the graph type.
        """
        self._config = config

    @final
    @property
    def config(self) -> C:
        """
        The config for the graph type.
        """
        return self._config

    @abstractmethod
    def build(self, df: pd.DataFrame) -> go.Figure:
        """
        Builds the graph type.
        
        Args:
            df: The pre-validated experiments dataframe.
            
        Returns:
            go.Figure: A plotly graph figure.
        """
        ...
