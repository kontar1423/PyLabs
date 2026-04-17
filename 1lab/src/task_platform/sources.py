from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from task_platform.models import Task


def _task_from_mapping(raw_task: Mapping[str, Any]) -> Task:
    try:
        task_id = raw_task["id"]
        payload = raw_task["payload"]
    except KeyError as error:
        raise ValueError("Each task must contain 'id' and 'payload' fields.") from error

    return Task(id=str(task_id), payload=payload)


@dataclass(frozen=True, slots=True)
class FileTaskSource:
    file_path: str | Path

    def get_tasks(self) -> list[Task]:
        content = Path(self.file_path).read_text(encoding="utf-8")
        data = json.loads(content)
        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of tasks.")

        return [_task_from_mapping(item) for item in data]


@dataclass(frozen=True, slots=True)
class GeneratorTaskSource:
    generator_factory: Callable[[], Iterable[Task]]

    def get_tasks(self) -> list[Task]:
        return list(self.generator_factory())


@dataclass(frozen=True, slots=True)
class ApiTaskSource:
    response: Sequence[Mapping[str, Any]]

    def get_tasks(self) -> list[Task]:
        return [_task_from_mapping(item) for item in self.response]
