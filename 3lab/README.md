# Лабораторная работа №3

Очередь задач для абстрактной платформы обработки задач.

## Что реализовано

- коллекция `TaskQueue` с поддержкой стандартной итерации;
- отдельный итератор с корректной обработкой `StopIteration`;
- повторный обход одной и той же очереди;
- ленивые фильтры по статусу и приоритету на основе генераторов;
- потоковая обработка задач без создания лишних списков;
- тесты с требуемым минимальным покрытием.

## Структура

- `src/task_platform/models.py` — модель задачи;
- `src/task_platform/queue.py` — очередь, итератор и ленивые операции;
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
from task_platform.queue import TaskQueue


queue = TaskQueue(
    [
        Task(id="task-1", status="new", priority=1, payload={"user": 1}),
        Task(id="task-2", status="done", priority=5, payload={"user": 2}),
    ]
)

print(list(queue))
print(list(queue.filter_by_status("done")))
print(list(queue.process(lambda task: task.id)))
```
