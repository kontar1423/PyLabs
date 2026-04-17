from __future__ import annotations

from datetime import datetime, timezone

import pytest

from task_platform.exceptions import (
    TaskDateError,
    TaskIdError,
    TaskPriorityError,
    TaskStatusError,
)
from task_platform.models import Task


def test_task_stores_valid_values_and_computed_properties() -> None:
    created_at = datetime(2026, 4, 17, 12, 0, tzinfo=timezone.utc)

    task = Task(
        id=" task-1 ",
        description=" Подготовить отчёт ",
        priority=3,
        status="new",
        created_at=created_at,
    )

    assert task.id == "task-1"
    assert task.description == "Подготовить отчёт"
    assert task.priority == 3
    assert task.status == "new"
    assert task.created_at == created_at
    assert task.is_ready is True
    assert task.label == "task-1: Подготовить отчёт"


def test_task_uses_private_internal_storage() -> None:
    task = Task(id="task-2", description="Проверить очередь", priority=2)

    assert task.__dict__["_id"] == "task-2"
    assert task.__dict__["_description"] == "Проверить очередь"
    assert task.__dict__["_priority"] == 2
    assert task.__dict__["_status"] == "new"
    assert "id" not in task.__dict__


def test_task_rejects_empty_id() -> None:
    with pytest.raises(TaskIdError):
        Task(id=" ", description="Описание", priority=2)


def test_task_rejects_invalid_priority() -> None:
    with pytest.raises(TaskPriorityError):
        Task(id="task-3", description="Описание", priority=10)


def test_task_rejects_invalid_status() -> None:
    with pytest.raises(TaskStatusError):
        Task(id="task-4", description="Описание", priority=1, status="archived")


def test_task_rejects_invalid_created_at() -> None:
    with pytest.raises(TaskDateError):
        Task(id="task-5", description="Описание", priority=1, created_at="today")  # type: ignore[arg-type]


def test_created_at_property_is_read_only() -> None:
    task = Task(id="task-6", description="Описание", priority=1)

    with pytest.raises(AttributeError):
        task.created_at = datetime.now(timezone.utc)  # type: ignore[misc]
