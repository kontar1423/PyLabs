from __future__ import annotations

from typing import Protocol, TypeGuard, runtime_checkable

from task_platform.models import Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> list[Task]:
        ...


def supports_task_source(source: object) -> TypeGuard[TaskSource]:
    return isinstance(source, TaskSource)
