from __future__ import annotations

from task_platform.contracts import supports_task_source
from task_platform.models import Task


class InvalidTaskSourceError(TypeError):
    pass


def collect_tasks(source: object) -> list[Task]:
    if not supports_task_source(source):
        message = (
            "Task source must implement get_tasks() and satisfy the TaskSource protocol."
        )
        raise InvalidTaskSourceError(message)

    return source.get_tasks()
