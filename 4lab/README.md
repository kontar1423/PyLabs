# Лабораторная работа №4

Асинхронный исполнитель задач для абстрактной платформы обработки задач.

## Что реализовано

- асинхронная очередь задач на `asyncio.Queue`;
- контракт обработчика через `typing.Protocol` с `@runtime_checkable`;
- `AsyncTaskExecutor` как асинхронный контекстный менеджер;
- централизованное логирование через стандартный `logging`;
- обработка ошибок: сбой обработчика не останавливает очередь.

## Структура

- `src/task_platform/models.py` — модель задачи;
- `src/task_platform/protocols.py` — контракт обработчика;
- `src/task_platform/handlers.py` — реализации обработчиков;
- `src/task_platform/executor.py` — асинхронный исполнитель;
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
import asyncio

from task_platform.executor import AsyncTaskExecutor
from task_platform.handlers import LoggingHandler
from task_platform.models import Task


async def main() -> None:
    handler = LoggingHandler()

    async with AsyncTaskExecutor(handler) as executor:
        executor.push(Task(id="task-1", status="new", priority=3, payload={"user": 1}))
        executor.push(Task(id="task-2", status="new", priority=5, payload={"user": 2}))
        await executor.run()


asyncio.run(main())
```
