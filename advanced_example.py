#!/usr/bin/env python3

from src.models import User, Task, TaskStatus
from src.core import TaskManager
from src.storage import DataStore
from datetime import datetime, timedelta
import json


def task_generator(tasks):
    """Generator that yields tasks one at a time."""
    # Si tasks es un dict, iterar sobre los valores
    if isinstance(tasks, dict):
        for task in tasks.values():
            yield task
    else:
        for task in tasks:
            yield task


def pending_task_generator(tasks):
    """Generator that filters and yields only pending tasks."""
    if isinstance(tasks, dict):
        values = tasks.values()
    else:
        values = tasks
    for task in values:
        if task.status == TaskStatus.PENDING:
            yield task


def task_batch_generator(tasks, batch_size=2):
    """Generator that yields tasks in batches."""
    if isinstance(tasks, dict):
        values = list(tasks.values())
    else:
        values = list(tasks)
    for i in range(0, len(values), batch_size):
        yield values[i : i + batch_size]


class TaskIterator:
    """Custom iterator for traversing tasks."""

    def __init__(self, tasks):
        if isinstance(tasks, dict):
            self.tasks = list(tasks.values())
        else:
            self.tasks = list(tasks)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.tasks):
            raise StopIteration
        result = self.tasks[self.index]
        self.index += 1
        return result


def demonstrate_generators():
    print("\n" + "=" * 60)
    print("Advanced Python Concepts - Generators & Iterators")
    print("=" * 60)

    manager = TaskManager()

    print("\n1. Creating sample data...")
    user1 = manager.add_user("Alice Engineer", "alice@example.com")
    user2 = manager.add_user("Bob Developer", "bob@example.com")

    for i in range(1, 6):
        manager.add_task(user1.user_id, f"Task {i}", f"Description for task {i}")

    for i in range(6, 9):
        manager.add_task(user2.user_id, f"Task {i}", f"Description for task {i}")

    first_task_id = next(iter(manager.tasks))
    manager.update_task_status(
        user1.user_id, first_task_id, TaskStatus.COMPLETED
    )
    # Actualiza el estado de la segunda tarea de user1 (si existe)
    user1_tasks = [t for t in manager.tasks.values() if t.user_id == user1.user_id]
    if len(user1_tasks) > 1:
        manager.update_task_status(user1.user_id, user1_tasks[1].task_id, TaskStatus.IN_PROGRESS)

    print(
        f"   Created {len(manager.users)} users with {len(manager.tasks)} total tasks"
    )

    print("\n2. Using basic generator (task_generator)...")
    print("   Iterating through all tasks:")
    count = 0
    for task in task_generator(manager.tasks):
        count += 1
        print(f"   - {task.title} ({task.status.value})")
        if count >= 3:
            print("   ... (showing first 3)")
            break

    print("\n3. Using filtered generator (pending_task_generator)...")
    print("   Iterating through pending tasks only:")
    for task in pending_task_generator(manager.tasks):
        print(f"   - {task.title}")

    print("\n4. Using batch generator (task_batch_generator)...")
    print("   Processing tasks in batches of 2:")
    for batch_num, batch in enumerate(
        task_batch_generator(manager.tasks, batch_size=2), 1
    ):
        print(f"   Batch {batch_num}: {len(batch)} tasks")
        for task in batch:
            print(f"     - {task.title}")

    print("\n5. Using custom iterator (TaskIterator)...")
    print("   Manual iteration through first 3 tasks:")
    iterator = TaskIterator(manager.tasks)
    for i in range(3):
        try:
            task = next(iterator)
            print(f"   {i + 1}. {task.title}")
        except StopIteration:
            print("   No more tasks")
            break

    print("\n6. Using list comprehension (Pythonic approach)...")
    print("   Extracting task titles and statuses:")
    task_info = [(t.title, t.status.value) for t in list(manager.tasks.values())[:4]]
    for title, status in task_info:
        print(f"   - {title}: {status}")

    print("\n7. Demonstrating string methods...")
    print("   Task title transformations:")
    task = list(manager.tasks.values())[0]
    print(f"   Original: '{task.title}'")
    print(f"   Upper: '{task.title.upper()}'")
    print(f"   Title case: '{task.title.title()}'")
    print(f"   Reversed: '{task.title[::-1]}'")
    print(f"   Starts with 'Task': {task.title.startswith('Task')}")

    print("\n8. Demonstrating list operations...")
    print("   Task list manipulations:")
    titles = [t.title for t in list(manager.tasks.values())]
    print(
        f"   Count of 'Task': {titles.count('Task 1' if 'Task 1' in titles else 'Task 5')}"
    )
    print(f"   Sorted titles (first 3): {sorted(titles)[:3]}")
    print(f"   Reversed (last 2): {list(reversed(titles))[-2:]}")

    print("\n9. Demonstrating datetime operations...")
    print("   Task creation and timing:")
    now = datetime.now()
    for i, task in enumerate(list(manager.tasks.values())[:3]):
        created = task.created_at
        elapsed = now - created
        print(f"   {task.title}: created {elapsed.total_seconds():.0f}s ago")

    print("\n10. Demonstrating file operations with JSON...")
    storage = DataStore()
    for user in manager.list_users():
        storage.add_user(user)
    for task in manager.list_tasks():
        storage.add_task(task)
    loaded_tasks = storage.list_tasks()
    print(f"    Saved and loaded {len(loaded_tasks)} tasks successfully from SQLite")

    print("\n" + "=" * 60)
    print("Advanced concepts demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_generators()
