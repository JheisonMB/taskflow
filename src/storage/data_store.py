"""Data persistence layer."""

import sqlite3
import os
from datetime import datetime
from typing import Optional

from src.core import TaskManager
from src.models import User, Task, TaskStatus

class DataStore:
    """Manages data persistence using SQLite."""

    def __init__(self, db_path: str = "data/tasks.db"):
        self.db_path = db_path
        data_dir = os.path.dirname(db_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self._init_db()

    def _init_db(self):
        """Create tables if they do not exist (migrations)."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            # Users table
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')
            # Tasks table
            c.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    assignee TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    completed_at TEXT,
                    FOREIGN KEY (assignee) REFERENCES users(user_id)
                )
            ''')
            conn.commit()

    # --- User CRUD ---
    def add_user(self, user: User) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (user_id, name, email) VALUES (?, ?, ?)",
                (user.user_id, user.name, user.email)
            )
            conn.commit()

    def get_user(self, user_id: str) -> Optional[User]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT user_id, name, email FROM users WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            if row:
                return User(row[1], row[2], row[0])
            return None

    def list_users(self) -> list:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT user_id, name, email FROM users")
            return [User(name, email, user_id) for user_id, name, email in c.fetchall()]

    # --- Task CRUD ---
    def add_task(self, task: Task) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                """
                INSERT INTO tasks (task_id, assignee, title, description, status, created_at, due_date, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task.task_id,
                    task.assignee,
                    task.title,
                    task.description,
                    task.status.value,
                    task.created_at.isoformat(),
                    task.due_date.isoformat(),
                    task.completed_at.isoformat() if task.completed_at else None
                )
            )
            conn.commit()

    def get_task(self, task_id: str) -> Optional[Task]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
            row = c.fetchone()
            if row:
                return self._row_to_task(row)
            return None

    def list_tasks(self) -> list:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM tasks")
            return [self._row_to_task(row) for row in c.fetchall()]

    def update_task_status(self, task_id: str, status: TaskStatus) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            completed_at = datetime.now().isoformat() if status == TaskStatus.COMPLETED else None
            c.execute(
                "UPDATE tasks SET status = ?, completed_at = ? WHERE task_id = ?",
                (status.value, completed_at, task_id)
            )
            conn.commit()

    def delete_task(self, task_id: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            conn.commit()

    # --- Helpers ---
    def _row_to_task(self, row) -> Task:
        (
            task_id, assignee, title, description, status, created_at,
            due_date, completed_at
        ) = row
        t = Task(
            assignee=assignee,
            title=title,
            description=description,
            due_date=datetime.fromisoformat(due_date),
            status=TaskStatus(status)
        )
        t.task_id = task_id
        t.created_at = datetime.fromisoformat(created_at)
        t.completed_at = datetime.fromisoformat(completed_at) if completed_at else None
        return t

    # --- Reports (archivos) ---
    def export_csv(self, tasks: list, filename: Optional[str] = None) -> bool:
        import csv
        try:
            if filename is None:
                filename = os.path.join(os.path.dirname(self.db_path), "tasks_export.csv")
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["task_id", "assignee", "title", "description", "status", "created_at", "due_date", "completed_at"])
                for t in tasks:
                    writer.writerow([
                        t.task_id,
                        t.assignee,
                        t.title,
                        t.description,
                        t.status.value,
                        t.created_at.isoformat(),
                        t.due_date.isoformat(),
                        t.completed_at.isoformat() if t.completed_at else ""
                    ])
            return True
        except Exception:
            return False

    def generate_report(self, tasks: list, users: list, filename: Optional[str] = None) -> bool:
        try:
            if filename is None:
                filename = os.path.join(os.path.dirname(self.db_path), f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write("TASK MANAGEMENT SYSTEM REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                f.write("USERS\n")
                f.write("=" * 80 + "\n")
                for user in users:
                    f.write(f"\n{user}\n")
                f.write("\n" + "=" * 80 + "\n")
                f.write("TASKS\n")
                f.write("=" * 80 + "\n")
                for task in tasks:
                    f.write(f"\n{task.task_id}: {task.title}\n")
                    f.write(f"  Status: {task.status.value}\n")
                    f.write(f"  Assignee: {task.assignee}\n")
                    f.write(f"  Description: {task.description}\n")
                    f.write(f"  Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}\n")
                    f.write(f"  Days remaining: {task.days_until_due()}\n")
            return True
        except Exception:
            return False
