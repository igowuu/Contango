from __future__ import annotations

from typing import Any, Callable, TypeVar

from contango.trading.analysis.graph_type import GraphType
from contango.trading.analysis.graph_config import GraphConfig


C = TypeVar("C", bound=GraphConfig)


GRAPH_REGISTRY: dict[str, type[GraphType[Any]]] = {}


def register_graph(name: str) -> Callable[[type[GraphType[C]]], type[GraphType[C]]]:
    """
    Registers a graph type with a name into registry.
    
    Args:
        name: The designated name for the graph type.
    """
    def decorator(cls: type[GraphType[C]]) -> type[GraphType[C]]:
        if name in GRAPH_REGISTRY:
            raise ValueError(f"Graph '{name}' already registered")

        cls.graph_name = name
        GRAPH_REGISTRY[name] = cls
        return cls
    return decorator
