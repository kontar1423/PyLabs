from __future__ import annotations

from types import GeneratorType

import pytest

from task_platform.models import Task
from task_platform.queue import TaskQueue


def build_queue() -> TaskQueue:
    return TaskQueue(
        [
            Task(id="task-1", status="new", priority=1, payload={"user": 1}),
            Task(id="task-2", status="done", priority=5, payload={"user": 2}),
            Task(id="task-3", status="in_progress", priority=3, payload={"user": 3}),
        ]
    )


def test_task_queue_supports_repeated_iteration() -> None:
    queue = build_queue()

    first_pass = [task.id for task in queue]
    second_pass = [task.id for task in queue]

    assert first_pass == ["task-1", "task-2", "task-3"]
    assert second_pass == first_pass


def test_task_queue_iterator_raises_stop_iteration() -> None:
    queue = build_queue()
    iterator = iter(queue)

    assert next(iterator).id == "task-1"
    assert next(iterator).id == "task-2"
    assert next(iterator).id == "task-3"

    with pytest.raises(StopIteration):
        next(iterator)


def test_filter_by_status_is_lazy_generator() -> None:
    queue = build_queue()
    filtered = queue.filter_by_status("done")

    queue.add(Task(id="task-4", status="done", priority=2, payload={"user": 4}))

    assert isinstance(filtered, GeneratorType)
    assert [task.id for task in filtered] == ["task-2", "task-4"]


def test_filter_by_priority_returns_matching_tasks() -> None:
    queue = build_queue()

    tasks = list(queue.filter_by_priority(minimum=2, maximum=4))

    assert tasks == [
        Task(id="task-3", status="in_progress", priority=3, payload={"user": 3})
    ]


def test_task_queue_is_compatible_with_list_and_sum() -> None:
    queue = build_queue()

    assert list(queue)[0].id == "task-1"
    assert sum(task.priority for task in queue) == 9


def test_process_streams_results_without_extra_collection() -> None:
    queue = build_queue()

    result = queue.process(lambda task: f"{task.id}:{task.status}")

    assert isinstance(result, GeneratorType)
    assert list(result) == [
        "task-1:new",
        "task-2:done",
        "task-3:in_progress",
    ]
