from __future__ import annotations

from typing import Any

from task_platform.exceptions import (
    TaskDescriptionError,
    TaskIdError,
    TaskPriorityError,
    TaskStatusError,
)


class ValidatedAttribute:
    def __init__(self, storage_name: str) -> None:
        self.storage_name = storage_name

    def __get__(self, instance: object | None, owner: type[object] | None = None) -> Any:
        if instance is None:
            return self

        return getattr(instance, self.storage_name)

    def __set__(self, instance: object, value: Any) -> None:
        setattr(instance, self.storage_name, self.validate(value))

    def validate(self, value: Any) -> Any:
        return value


class TaskIdDescriptor(ValidatedAttribute):
    def validate(self, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise TaskIdError("Task id must be a non-empty string.")

        return value.strip()


class TaskDescriptionDescriptor(ValidatedAttribute):
    def validate(self, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise TaskDescriptionError("Task description must be a non-empty string.")

        return value.strip()


class TaskPriorityDescriptor(ValidatedAttribute):
    def validate(self, value: Any) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TaskPriorityError("Task priority must be an integer from 1 to 5.")

        if not 1 <= value <= 5:
            raise TaskPriorityError("Task priority must be in range from 1 to 5.")

        return value


class TaskStatusDescriptor(ValidatedAttribute):
    allowed_statuses = {"new", "in_progress", "done", "cancelled"}

    def validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise TaskStatusError("Task status must be a string.")

        normalized_value = value.strip()
        if normalized_value not in self.allowed_statuses:
            raise TaskStatusError(
                "Task status must be one of: new, in_progress, done, cancelled."
            )

        return normalized_value


class TaskLabelDescriptor:
    def __get__(self, instance: object | None, owner: type[object] | None = None) -> str | TaskLabelDescriptor:
        if instance is None:
            return self

        return f"{instance.id}: {instance.description}"
