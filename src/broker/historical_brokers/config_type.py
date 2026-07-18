from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Config:
    """
    Marks a dataclass as a configurator for a historical broker when deriving data from it.
    """
    ...
