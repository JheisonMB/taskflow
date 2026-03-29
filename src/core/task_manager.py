"""Task manager - central system management."""

from datetime import datetime
from typing import List, Optional, Iterator

from src.models import User, Task, TaskStatus


class TaskManager:
    """Central task management system."""

    def __init__(self):
        self.users: dict[str, User] = {}
        self.tasks: dict[str, Task] = {}
        self._task_counter = 0

    def add_user(self, name: str, email: str) -> User:
        """Add a new user."""
        user = User(name, email)
        self.users[user.user_id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)

    def list_users(self) -> List[User]:
        """Get all users."""
        return list(self.users.values())

    def add_task(self, assignee: str, title: str, description: str, due_date=None) -> Task:
        """Add a new task."""
        if assignee not in self.users:
            raise ValueError(f"User {assignee!r} not found")
        from datetime import datetime
        due_date = due_date or datetime.now()
        task = Task(assignee, title, description, due_date)
        self.tasks[task.task_id] = task
        self.users[assignee].add_task(task.task_id)
        return task

    def get_task(self, user_id: str, task_id: str) -> Optional[Task]:
        """Get task by ID for a user."""
        task = self.tasks.get(task_id)
        if task and task.assignee == user_id:
            return task
        return None

    def list_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self.tasks.values())

    def delete_task(self, user_id: str, task_id: str) -> bool:
        """Delete a task if it belongs to the user."""
        task = self.tasks.get(task_id)
        if not task or task.assignee != user_id:
            return False
        del self.tasks[task_id]
        self.users[user_id].remove_task(task_id)
        return True

    def update_task_status(self, user_id: str, task_id: str, status: TaskStatus) -> bool:
        """Update task status."""
        if task_id not in self.tasks:
            return False
        if self.tasks[task_id].assignee != user_id:
            return False
        self.tasks[task_id].set_status(status)
        return True

    def filter_tasks_by_status(self, status: TaskStatus) -> list:
        """Return all tasks with a given status."""
        return [t for t in self.tasks.values() if t.status == status]

    def filter_by_status(self, status: TaskStatus) -> List[Task]:
        """Filter tasks by status."""
        return [t for t in self.tasks.values() if t.status == status]

    def get_user_tasks(self, user_id: str) -> list:
        """Return all tasks assigned to a user."""
        return [t for t in self.tasks.values() if t.assignee == user_id]

    def filter_by_assignee(self, user_id: str) -> List[Task]:
        """Filter tasks by assignee."""
        if user_id not in self.users:
            return []
        return [t for t in self.tasks.values() if t.assignee == user_id]

    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks."""
        return [t for t in self.tasks.values() if t.is_overdue()]

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get tasks due within N days."""
        result = []
        now = datetime.now()
        for task in self.tasks.values():
            days_remaining = (task.due_date - now).days
            if 0 <= days_remaining <= days and task.status != TaskStatus.COMPLETED:
                result.append(task)
        return result

    def iter_user_tasks(self, user_id: str) -> Iterator[Task]:
        """Generate tasks for a user."""
        if user_id not in self.users:
            return
        for task_id in self.users[user_id].get_tasks():
            if task_id in self.tasks:
                yield self.tasks[task_id]

    def iter_all_tasks(self) -> Iterator[Task]:
        """Generate all tasks."""
        for task in self.tasks.values():
            yield task

    def iter_users(self) -> Iterator[User]:
        """Generate all users."""
        for user in self.users.values():
            yield user

    def get_stats(self) -> dict:
        """Get system statistics."""
        total_tasks = len(self.tasks)
        pending = len(self.filter_by_status(TaskStatus.PENDING))
        in_progress = len(self.filter_by_status(TaskStatus.IN_PROGRESS))
        completed = len(self.filter_by_status(TaskStatus.COMPLETED))
        overdue = len(self.get_overdue_tasks())

        return {
            "total_users": len(self.users),
            "total_tasks": total_tasks,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "overdue": overdue,
            "completion_rate": (completed / total_tasks * 100) if total_tasks else 0,
        }

    def get_user_stats(self, user_id: str) -> Optional[dict]:
        """Get user statistics."""
        if user_id not in self.users:
            return None

        user = self.users[user_id]
        tasks = self.filter_by_assignee(user_id)

        pending = len([t for t in tasks if t.status == TaskStatus.PENDING])
        in_progress = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])
        completed = len([t for t in tasks if t.status == TaskStatus.COMPLETED])

        return {
            "user": user.name,
            "total_tasks": len(tasks),
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "completion_rate": (completed / len(tasks) * 100) if tasks else 0,
        }
