"""Task model for task management system."""

from datetime import datetime
from .task_status import TaskStatus


class Task:
    """Represents a system task."""

    def __init__(
        self,
        assignee: str,
        title: str,
        description: str,
        due_date: datetime = None,
        status: TaskStatus = TaskStatus.PENDING,
    ):
        import uuid
        self.task_id = str(uuid.uuid4())
        self.user_id = assignee
        self.title = title.strip()
        self.description = description.strip()
        self.assignee = assignee
        self.created_at = datetime.now()
        self.due_date = due_date if due_date else self.created_at
        self.status = status
        self.completed_at = None

    def set_status(self, status: TaskStatus) -> None:
        self.status = status
        if status == TaskStatus.COMPLETED:
            self.completed_at = datetime.now()
        else:
            self.completed_at = None

    def reassign(self, new_assignee: str) -> None:
        self.assignee = new_assignee

    def days_until_due(self) -> int:
        delta = self.due_date - datetime.now()
        return delta.days

    def is_overdue(self) -> bool:
        return datetime.now() > self.due_date and self.status != TaskStatus.COMPLETED

    def __str__(self) -> str:
        return f"[{self.status.value.upper()}] {self.title}"

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "user_id": self.assignee,
            "title": self.title,
            "description": self.description,
            "assignee": self.assignee,
            "created_at": self.created_at.isoformat(),
            "due_date": self.due_date.isoformat(),
            "status": self.status.value,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        task = cls(
            data["task_id"],
            data["title"],
            data["description"],
            data["assignee"],
            datetime.fromisoformat(data["due_date"]),
            TaskStatus(data["status"]),
        )
        task.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("completed_at"):
            task.completed_at = datetime.fromisoformat(data["completed_at"])
        return task
