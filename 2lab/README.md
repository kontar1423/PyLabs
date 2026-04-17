# Лабораторная работа №2

Модель задачи для абстрактной платформы обработки задач.

## Что реализовано

- класс `Task` с инкапсуляцией внутреннего состояния;
- пользовательские дескрипторы для валидации `id`, `description`, `priority` и `status`;
- `@property` для вычисляемого признака готовности и защищённого времени создания;
- специализированные исключения при нарушении инвариантов;
- демонстрация различий между data и non-data descriptors;
- тесты с требуемым минимальным покрытием.

## Структура

- `src/task_platform/models.py` — модель задачи;
- `src/task_platform/descriptors.py` — дескрипторы для проверки атрибутов;
- `src/task_platform/exceptions.py` — пользовательские исключения;
- `tests/` — тесты.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Пример

```python
from task_platform.models import Task


task = Task(
    id="task-1",
    description="Подготовить отчёт",
    priority=3,
    status="new",
)

print(task.label)
print(task.is_ready)
print(task.created_at)
```
