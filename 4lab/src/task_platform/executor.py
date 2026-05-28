from __future__ import annotations

import asyncio
import logging
from typing import Any

from task_platform.models import Task
from task_platform.protocols import TaskHandler

logger = logging.getLogger(__name__)


class AsyncTaskExecutor:
    def __init__(self, handler: TaskHandler) -> None:
        self._queue: asyncio.Queue[Task] = asyncio.Queue()
        self._handler = handler

    def push(self, task: Task) -> None:
        self._queue.put_nowait(task)

    async def pop(self) -> Task:
        return await self._queue.get()

    async def run(self) -> None:
        while not self._queue.empty():
            task = await self.pop()

            try:
                await self._handler.handle(task)
            except Exception:
                logger.exception("Task %s failed", task.id)

    async def __aenter__(self) -> AsyncTaskExecutor:
        return self

    async def __aexit__(self, *args: Any) -> None:
        pass
