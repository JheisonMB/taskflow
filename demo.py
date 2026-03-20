#!/usr/bin/env python3

from src.models import User, Task, TaskStatus
from src.core import TaskManager
from src.storage import DataStore
from datetime import datetime, timedelta


def main():
    print("=" * 60)
    print("Task Management System - Demo")
    print("=" * 60)

    manager = TaskManager()
    storage = DataStore()

    print("\n1. Creating users...")
    user1 = manager.add_user("Alice Johnson", "alice@example.com")
    user2 = manager.add_user("Bob Smith", "bob@example.com")
    print(f"   Created: {user1.name} ({user1.email})")
    print(f"   Created: {user2.name} ({user2.email})")

    print("\n2. Adding tasks for Alice...")
    task1 = manager.add_task(
        user1.user_id, "Implement authentication", "Set up JWT tokens"
    )
    task2 = manager.add_task(
        user1.user_id, "Write unit tests", "Add tests for core module"
    )
    task3 = manager.add_task(
        user1.user_id, "Deploy to production", "Release version 1.0"
    )
    print(f"   Added: {task1.title} (ID: {task1.task_id})")
    print(f"   Added: {task2.title} (ID: {task2.task_id})")
    print(f"   Added: {task3.title} (ID: {task3.task_id})")

    print("\n3. Adding tasks for Bob...")
    task4 = manager.add_task(user2.user_id, "Code review", "Review pull requests")
    task5 = manager.add_task(user2.user_id, "Update documentation", "Add API docs")
    print(f"   Added: {task4.title} (ID: {task4.task_id})")
    print(f"   Added: {task5.title} (ID: {task5.task_id})")

    print("\n4. Updating task statuses...")
    manager.update_task_status(user1.user_id, task1.task_id, TaskStatus.IN_PROGRESS)
    manager.update_task_status(user1.user_id, task2.task_id, TaskStatus.COMPLETED)
    print(f"   {task1.title}: {TaskStatus.IN_PROGRESS.value}")
    print(f"   {task2.title}: {TaskStatus.COMPLETED.value}")

    print("\n5. Viewing all tasks for Alice...")
    alice_tasks = manager.get_user_tasks(user1.user_id)
    for task in alice_tasks:
        print(f"   - {task.title}: {task.status.value}")

    print("\n6. Filtering completed tasks...")
    completed = manager.filter_tasks_by_status(TaskStatus.COMPLETED)
    for task in completed:
        print(f"   - {task.title} (by {task.user_id})")

    print("\n7. Persisting data...")
    storage.save_users_json(manager.users, "users.json")
    storage.save_tasks_pickle(manager.tasks, "tasks.pkl")
    storage.save_tasks_csv(manager.tasks, "tasks.csv")
    print("   Saved to: users.json, tasks.pkl, tasks.csv")

    print("\n8. Generating text report...")
    report = storage.generate_text_report(manager.users, manager.tasks)
    print(report)

    print("\n9. Loading data from storage...")
    loaded_users = storage.load_users_json("users.json")
    loaded_tasks = storage.load_tasks_pickle("tasks.pkl")
    print(f"   Loaded {len(loaded_users)} users and {len(loaded_tasks)} tasks")

    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
