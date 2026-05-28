from __future__ import annotations

import asyncio
import logging

from task_platform.models import Task

logger = logging.getLogger(__name__)


class LoggingHandler:
    async def handle(self, task: Task) -> None:
        logger.info("Processing task %s (status=%s, priority=%d)", task.id, task.status, task.priority)
        await asyncio.sleep(0)


class CollectingHandler:
    def __init__(self) -> None:
        self._results: list[Task] = []

    async def handle(self, task: Task) -> None:
        await asyncio.sleep(0)
        self._results.append(task)

    @property
    def results(self) -> list[Task]:
        return list(self._results)
