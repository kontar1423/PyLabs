from __future__ import annotations

import pytest

from task_platform.exceptions import TaskPriorityError
from task_platform.models import Task


def test_data_descriptor_validates_reassignment() -> None:
    task = Task(id="task-1", description="Описание", priority=2)

    with pytest.raises(TaskPriorityError):
        task.priority = 0


def test_non_data_descriptor_can_be_shadowed_by_instance_attribute() -> None:
    task = Task(id="task-2", description="Подготовить данные", priority=4)

    task.label = "Временная подпись"

    assert task.label == "Временная подпись"
    assert Task.label.__get__(task, Task) == "task-2: Подготовить данные"
