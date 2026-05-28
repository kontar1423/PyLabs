from __future__ import annotations

from typing import Protocol, runtime_checkable

from task_platform.models import Task


@runtime_checkable
class TaskHandler(Protocol):
    async def handle(self, task: Task) -> None:
        ...
