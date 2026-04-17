# Лабораторная работа №1

Подсистема приёма задач для абстрактной платформы обработки задач.

## Что реализовано

- единый контракт источника задач через `typing.Protocol`;
- runtime-проверка контракта через `@runtime_checkable` и `isinstance()`;
- независимые источники задач без общего базового класса;
- модуль приёма задач, работающий с любым источником, который соблюдает контракт;
- тесты с требуемым минимальным покрытием.

## Структура

- `src/task_platform/models.py` — модель задачи;
- `src/task_platform/contracts.py` — контракт источника и проверки;
- `src/task_platform/sources.py` — реализации источников;
- `src/task_platform/receiver.py` — функция приёма задач;
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
from task_platform.receiver import collect_tasks
from task_platform.sources import GeneratorTaskSource
from task_platform.models import Task


source = GeneratorTaskSource(
    lambda: (Task(id=f"task-{index}", payload={"index": index}) for index in range(3))
)

tasks = collect_tasks(source)
print(tasks)
```
