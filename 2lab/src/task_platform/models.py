from __future__ import annotations

from datetime import datetime, timezone

from task_platform.descriptors import (
    TaskDescriptionDescriptor,
    TaskIdDescriptor,
    TaskLabelDescriptor,
    TaskPriorityDescriptor,
    TaskStatusDescriptor,
)
from task_platform.exceptions import TaskDateError


class Task:
    id = TaskIdDescriptor("_id")
    description = TaskDescriptionDescriptor("_description")
    priority = TaskPriorityDescriptor("_priority")
    status = TaskStatusDescriptor("_status")
    label = TaskLabelDescriptor()

    def __init__(
        self,
        id: str,
        description: str,
        priority: int,
        status: str = "new",
        created_at: datetime | None = None,
    ) -> None:
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self._created_at = self._validate_created_at(created_at)

    @staticmethod
    def _validate_created_at(value: datetime | None) -> datetime:
        if value is None:
            return datetime.now(timezone.utc)

        if not isinstance(value, datetime):
            raise TaskDateError("created_at must be a datetime object.")

        return value

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def is_ready(self) -> bool:
        return self.status == "new"

    def __repr__(self) -> str:
        return (
            "Task("
            f"id={self.id!r}, "
            f"description={self.description!r}, "
            f"priority={self.priority!r}, "
            f"status={self.status!r}"
            ")"
        )
