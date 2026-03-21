"""Data persistence layer."""

import json
import pickle
import os
from datetime import datetime
from typing import Optional

from src.core import TaskManager
from src.models import User, Task


class DataStore:
    """Manages data persistence."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.json_file = os.path.join(data_dir, "tasks.json")
        self.pickle_file = os.path.join(data_dir, "tasks.pkl")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def save_json(self, manager: TaskManager) -> bool:
        """Save to JSON format."""
        try:
            data = {
                "exported_at": datetime.now().isoformat(),
                "users": [u.to_dict() for u in manager.list_users()],
                "tasks": [t.to_dict() for t in manager.list_tasks()],
            }
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False

    def load_json(self, manager: TaskManager) -> bool:
        """Load from JSON format."""
        try:
            if not os.path.exists(self.json_file):
                return False

            with open(self.json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for user_data in data.get("users", []):
                user = User.from_dict(user_data)
                manager.users[user.user_id] = user

            for task_data in data.get("tasks", []):
                task = Task.from_dict(task_data)
                manager.tasks[task.task_id] = task

                if task.task_id.startswith("TASK-"):
                    try:
                        num = int(task.task_id.split("-")[1])
                        manager._task_counter = max(manager._task_counter, num)
                    except ValueError:
                        pass

            return True
        except Exception:
            return False

    def save_pickle(self, manager: TaskManager) -> bool:
        """Save to pickle format."""
        try:
            data = {
                "exported_at": datetime.now(),
                "users": {uid: u.to_dict() for uid, u in manager.users.items()},
                "tasks": {tid: t.to_dict() for tid, t in manager.tasks.items()},
                "task_counter": manager._task_counter,
            }
            with open(self.pickle_file, "wb") as f:
                pickle.dump(data, f)
            return True
        except Exception:
            return False

    def load_pickle(self, manager: TaskManager) -> bool:
        """Load from pickle format."""
        try:
            if not os.path.exists(self.pickle_file):
                return False

            with open(self.pickle_file, "rb") as f:
                data = pickle.load(f)

            for user_data in data.get("users", {}).values():
                user = User.from_dict(user_data)
                manager.users[user.user_id] = user

            for task_data in data.get("tasks", {}).values():
                task = Task.from_dict(task_data)
                manager.tasks[task.task_id] = task

            manager._task_counter = data.get("task_counter", 0)
            return True
        except Exception:
            return False

    def export_csv(self, manager: TaskManager, filename: Optional[str] = None) -> bool:
        """Export tasks to CSV."""
        try:
            if filename is None:
                filename = os.path.join(self.data_dir, "tasks_export.csv")

            with open(filename, "w", encoding="utf-8") as f:
                f.write(
                    "ID,Title,Description,Assignee,Status,Created,Due,Days Remaining\n"
                )

                for task in manager.list_tasks():
                    line = (
                        f'"{task.task_id}",'
                        f'"{task.title}",'
                        f'"{task.description}",'
                        f'"{task.assignee}",'
                        f'"{task.status.value}",'
                        f'"{task.created_at.strftime("%Y-%m-%d %H:%M")}",'
                        f'"{task.due_date.strftime("%Y-%m-%d %H:%M")}",'
                        f'"{task.days_until_due()}"\n'
                    )
                    f.write(line)

            return True
        except Exception:
            return False

    def generate_report(
        self, manager: TaskManager, filename: Optional[str] = None
    ) -> bool:
        """Generate text report."""
        try:
            if filename is None:
                filename = os.path.join(
                    self.data_dir,
                    f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                )

            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write("TASK MANAGEMENT SYSTEM REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                stats = manager.get_stats()
                f.write("SYSTEM STATISTICS\n")
                f.write("-" * 80 + "\n")
                for key, value in stats.items():
                    if "rate" in key:
                        f.write(f"{key}: {value:.1f}%\n")
                    else:
                        f.write(f"{key}: {value}\n")

                f.write("\n" + "=" * 80 + "\n")
                f.write("USERS\n")
                f.write("=" * 80 + "\n")
                for user in manager.iter_users():
                    stats_u = manager.get_user_stats(user.user_id)
                    f.write(f"\n{user}\n")
                    f.write(f"  Assigned tasks: {stats_u['total_tasks']}\n")
                    f.write(f"  Completion rate: {stats_u['completion_rate']:.1f}%\n")

                f.write("\n" + "=" * 80 + "\n")
                f.write("TASKS\n")
                f.write("=" * 80 + "\n")
                for task in manager.iter_all_tasks():
                    f.write(f"\n{task.task_id}: {task.title}\n")
                    f.write(f"  Status: {task.status.value}\n")
                    f.write(f"  Assignee: {task.assignee}\n")
                    f.write(f"  Description: {task.description}\n")
                    f.write(f"  Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}\n")
                    f.write(f"  Days remaining: {task.days_until_due()}\n")

            return True
        except Exception:
            return False
