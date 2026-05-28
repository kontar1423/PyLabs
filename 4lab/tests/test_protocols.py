from __future__ import annotations

from task_platform.handlers import CollectingHandler, LoggingHandler
from task_platform.protocols import TaskHandler


def test_collecting_handler_satisfies_protocol() -> None:
    assert isinstance(CollectingHandler(), TaskHandler)


def test_logging_handler_satisfies_protocol() -> None:
    assert isinstance(LoggingHandler(), TaskHandler)
