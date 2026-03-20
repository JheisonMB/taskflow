"""User model for task management system."""


class User:
    """Represents a system user."""

    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name.strip()
        self.email = email.strip()
        self.assigned_tasks = []

    def add_task(self, task_id: str) -> None:
        if task_id not in self.assigned_tasks:
            self.assigned_tasks.append(task_id)

    def remove_task(self, task_id: str) -> None:
        if task_id in self.assigned_tasks:
            self.assigned_tasks.remove(task_id)

    def get_tasks(self) -> list:
        return self.assigned_tasks.copy()

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "assigned_tasks": self.assigned_tasks.copy(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(data["user_id"], data["name"], data["email"])
        user.assigned_tasks = data.get("assigned_tasks", [])
        return user
