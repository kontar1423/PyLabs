from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar

from task_platform.models import Task

T = TypeVar("T")


class TaskQueueIterator:
    def __init__(self, tasks: list[Task]) -> None:
        self._tasks = tasks
        self._index = 0

    def __iter__(self) -> TaskQueueIterator:
        return self

    def __next__(self) -> Task:
        if self._index >= len(self._tasks):
            raise StopIteration

        task = self._tasks[self._index]
        self._index += 1
        return task


class TaskQueue:
    def __init__(self, tasks: Iterable[Task] = ()) -> None:
        self._tasks = list(tasks)

    def add(self, task: Task) -> None:
        self._tasks.append(task)

    def __iter__(self) -> TaskQueueIterator:
        return TaskQueueIterator(self._tasks)

    def __len__(self) -> int:
        return len(self._tasks)

    def filter_by_status(self, status: str) -> Iterator[Task]:
        for task in self:
            if task.status == status:
                yield task

    def filter_by_priority(
        self,
        minimum: int | None = None,
        maximum: int | None = None,
    ) -> Iterator[Task]:
        for task in self:
            if minimum is not None and task.priority < minimum:
                continue

            if maximum is not None and task.priority > maximum:
                continue

            yield task

    def process(self, handler: Callable[[Task], T]) -> Iterator[T]:
        for task in self:
            yield handler(task)
