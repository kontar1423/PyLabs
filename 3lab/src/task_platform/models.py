from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Task:
    id: str
    status: str
    priority: int
    payload: Any
