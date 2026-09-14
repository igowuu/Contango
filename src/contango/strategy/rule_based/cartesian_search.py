from __future__ import annotations

from functools import partial
from itertools import product
from typing import Any, Callable, Iterator, Mapping, Sequence, Type, TypeVar


StrategyT = TypeVar("StrategyT")


def cartesian_search(
    strategy_cls: Type[StrategyT],
    param_grid: Mapping[str, Sequence[Any]],
) -> Iterator[tuple[Callable[[], StrategyT], dict[str, Any]]]:
    """
    Generates every parameter combination for a strategy class.
    
    Args:
        strategy_cls: The strategy to perform a Cartesian search on.
        param_grid: A mapping of strings to sequences of values to be 
                    tested and parameterized into the strategy cls.
    
    Yields:
        A tuple of `(factory, kwargs)`, where factory is a callable that
        constructs `strategy_cls(**kwargs)`.
    """
    keys = list(param_grid.keys())
    for combo in product(*param_grid.values()):
        kwargs = dict(zip(keys, combo))
        yield partial(strategy_cls, **kwargs), kwargs
