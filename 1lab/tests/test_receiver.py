from __future__ import annotations

import pytest

from task_platform.models import Task
from task_platform.receiver import InvalidTaskSourceError, collect_tasks


class CustomSource:
    def get_tasks(self) -> list[Task]:
        return [
            Task(id="custom-1", payload={"type": "custom"}),
            Task(id="custom-2", payload={"type": "custom"}),
        ]


class BrokenSource:
    pass


def test_collect_tasks_returns_tasks_from_valid_source() -> None:
    tasks = collect_tasks(CustomSource())

    assert tasks == [
        Task(id="custom-1", payload={"type": "custom"}),
        Task(id="custom-2", payload={"type": "custom"}),
    ]


def test_collect_tasks_raises_for_invalid_source() -> None:
    with pytest.raises(InvalidTaskSourceError):
        collect_tasks(BrokenSource())


def test_collect_tasks_error_has_clear_message() -> None:
    with pytest.raises(InvalidTaskSourceError) as error:
        collect_tasks(BrokenSource())

    assert "TaskSource protocol" in str(error.value)
