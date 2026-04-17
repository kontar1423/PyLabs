from __future__ import annotations

from task_platform.contracts import TaskSource, supports_task_source
from task_platform.models import Task
from task_platform.sources import GeneratorTaskSource


class AdHocSource:
    def get_tasks(self) -> list[Task]:
        return [Task(id="adhoc-1", payload={"status": "ok"})]


class InvalidSource:
    def tasks(self) -> list[Task]:
        return []


def test_supports_task_source_accepts_duck_typed_object() -> None:
    source = AdHocSource()

    assert supports_task_source(source) is True
    assert isinstance(source, TaskSource)


def test_generator_source_matches_protocol_on_class_level() -> None:
    assert issubclass(GeneratorTaskSource, TaskSource)


def test_supports_task_source_rejects_invalid_object() -> None:
    source = InvalidSource()

    assert supports_task_source(source) is False
    assert isinstance(source, TaskSource) is False
