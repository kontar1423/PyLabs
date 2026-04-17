from __future__ import annotations

import json

import pytest

from task_platform.models import Task
from task_platform.sources import ApiTaskSource, FileTaskSource, GeneratorTaskSource


def test_file_task_source_reads_tasks_from_json(tmp_path) -> None:
    task_file = tmp_path / "tasks.json"
    task_file.write_text(
        json.dumps(
            [
                {"id": "file-1", "payload": {"priority": "high"}},
                {"id": "file-2", "payload": [1, 2, 3]},
            ]
        ),
        encoding="utf-8",
    )

    source = FileTaskSource(task_file)

    assert source.get_tasks() == [
        Task(id="file-1", payload={"priority": "high"}),
        Task(id="file-2", payload=[1, 2, 3]),
    ]


def test_file_task_source_rejects_non_list_json(tmp_path) -> None:
    task_file = tmp_path / "tasks.json"
    task_file.write_text(json.dumps({"id": "single-task"}), encoding="utf-8")

    source = FileTaskSource(task_file)

    with pytest.raises(ValueError):
        source.get_tasks()


def test_generator_task_source_materializes_factory_output() -> None:
    source = GeneratorTaskSource(
        lambda: (Task(id=f"generated-{index}", payload=index) for index in range(3))
    )

    assert source.get_tasks() == [
        Task(id="generated-0", payload=0),
        Task(id="generated-1", payload=1),
        Task(id="generated-2", payload=2),
    ]


def test_api_task_source_converts_stub_payloads_to_tasks() -> None:
    source = ApiTaskSource(
        response=[
            {"id": "api-1", "payload": {"source": "stub"}},
            {"id": 42, "payload": "ready"},
        ]
    )

    assert source.get_tasks() == [
        Task(id="api-1", payload={"source": "stub"}),
        Task(id="42", payload="ready"),
    ]


def test_api_task_source_raises_on_invalid_payload_shape() -> None:
    source = ApiTaskSource(response=[{"payload": "missing id"}])

    with pytest.raises(ValueError):
        source.get_tasks()
