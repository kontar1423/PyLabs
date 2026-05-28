from __future__ import annotations

from task_platform.executor import AsyncTaskExecutor
from task_platform.handlers import CollectingHandler
from task_platform.models import Task


async def test_executor_processes_tasks() -> None:
    handler = CollectingHandler()

    async with AsyncTaskExecutor(handler) as executor:
        executor.push(Task(id="task-1", status="new", priority=1, payload={}))
        executor.push(Task(id="task-2", status="new", priority=2, payload={}))
        await executor.run()

    assert handler.results == [
        Task(id="task-1", status="new", priority=1, payload={}),
        Task(id="task-2", status="new", priority=2, payload={}),
    ]


async def test_executor_continues_after_handler_exception() -> None:
    class FailOnceHandler:
        def __init__(self) -> None:
            self.results: list[Task] = []
            self._failed = False

        async def handle(self, task: Task) -> None:
            if not self._failed:
                self._failed = True
                msg = f"Handler failed for {task.id}"
                raise RuntimeError(msg)
            self.results.append(task)

    handler = FailOnceHandler()

    async with AsyncTaskExecutor(handler) as executor:
        executor.push(Task(id="task-1", status="new", priority=1, payload={}))
        executor.push(Task(id="task-2", status="new", priority=2, payload={}))
        await executor.run()

    assert len(handler.results) == 1
    assert handler.results[0].id == "task-2"


async def test_executor_pop_returns_task() -> None:
    handler = CollectingHandler()
    executor = AsyncTaskExecutor(handler)
    executor.push(Task(id="task-1", status="new", priority=1, payload={}))

    task = await executor.pop()
    assert task.id == "task-1"
