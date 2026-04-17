from __future__ import annotations


class TaskValidationError(ValueError):
    pass


class TaskIdError(TaskValidationError):
    pass


class TaskDescriptionError(TaskValidationError):
    pass


class TaskPriorityError(TaskValidationError):
    pass


class TaskStatusError(TaskValidationError):
    pass


class TaskDateError(TaskValidationError):
    pass
