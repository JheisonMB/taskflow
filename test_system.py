import os
import pytest
from src.models import User, Task, TaskStatus
from src.core import TaskManager
from src.storage import DataStore

# --- User tests ---
def test_user_creation():
    user = User("John Doe", "john@example.com")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.user_id is not None

def test_user_to_dict():
    user = User("Jane Smith", "jane@example.com")
    user_dict = user.to_dict()
    assert "user_id" in user_dict
    assert "name" in user_dict
    assert "email" in user_dict
    assert user_dict["name"] == "Jane Smith"

# --- Task tests ---
def test_task_creation():
    task = Task("user123", "Complete project", "Finish the final deliverable")
    assert task.title == "Complete project"
    assert task.description == "Finish the final deliverable"
    assert task.status == TaskStatus.PENDING
    assert task.task_id is not None

def test_task_status_change():
    task = Task("user123", "Review code", "Review PR #42")
    assert task.status == TaskStatus.PENDING
    task.status = TaskStatus.IN_PROGRESS
    assert task.status == TaskStatus.IN_PROGRESS
    task.status = TaskStatus.COMPLETED
    assert task.status == TaskStatus.COMPLETED

def test_task_to_dict():
    task = Task("user456", "Write docs", "Add API documentation")
    task_dict = task.to_dict()
    assert "task_id" in task_dict
    assert "user_id" in task_dict
    assert "title" in task_dict
    assert "status" in task_dict
    assert task_dict["user_id"] == "user456"

# --- TaskManager tests ---
@pytest.fixture
def manager():
    return TaskManager()

def test_add_user(manager):
    user = manager.add_user("Alice Wonder", "alice@example.com")
    assert user.name == "Alice Wonder"
    assert len(manager.users) == 1

def test_add_multiple_users(manager):
    user1 = manager.add_user("Bob Builder", "bob@example.com")
    user2 = manager.add_user("Carol Davis", "carol@example.com")
    assert len(manager.users) == 2
    assert user1.user_id != user2.user_id

def test_add_task(manager):
    user = manager.add_user("David Lee", "david@example.com")
    task = manager.add_task(user.user_id, "Test task", "Description here")
    assert task.user_id == user.user_id
    assert len(manager.tasks) == 1

def test_get_user_tasks(manager):
    user = manager.add_user("Eve Miller", "eve@example.com")
    manager.add_task(user.user_id, "Task 1", "First task")
    manager.add_task(user.user_id, "Task 2", "Second task")
    user_tasks = manager.get_user_tasks(user.user_id)
    assert len(user_tasks) == 2

def test_update_task_status(manager):
    user = manager.add_user("Frank Wilson", "frank@example.com")
    task = manager.add_task(user.user_id, "Status test", "Test updating status")
    manager.update_task_status(user.user_id, task.task_id, TaskStatus.IN_PROGRESS)
    updated_task = manager.get_task(user.user_id, task.task_id)
    assert updated_task.status == TaskStatus.IN_PROGRESS

def test_filter_tasks_by_status(manager):
    user1 = manager.add_user("Grace Lee", "grace@example.com")
    user2 = manager.add_user("Henry Brown", "henry@example.com")
    task1 = manager.add_task(user1.user_id, "Completed task", "Done")
    manager.add_task(user2.user_id, "Pending task", "Not started")
    manager.update_task_status(user1.user_id, task1.task_id, TaskStatus.COMPLETED)
    completed_tasks = manager.filter_tasks_by_status(TaskStatus.COMPLETED)
    assert len(completed_tasks) == 1
    assert completed_tasks[0].task_id == task1.task_id

def test_delete_task(manager):
    user = manager.add_user("Iris White", "iris@example.com")
    task = manager.add_task(user.user_id, "To delete", "This task will be deleted")
    assert len(manager.tasks) == 1
    manager.delete_task(user.user_id, task.task_id)
    assert len(manager.tasks) == 0

def test_get_task(manager):
    user = manager.add_user("Jack Martin", "jack@example.com")
    task = manager.add_task(user.user_id, "Find me", "Retrieve this task")
    retrieved = manager.get_task(user.user_id, task.task_id)
    assert retrieved.task_id == task.task_id
    assert retrieved.title == "Find me"

# --- DataStore tests ---
@pytest.fixture
def storage():
    return DataStore()

def test_add_and_list_users(storage):
    user1 = User("Kate Wilson", "kate@example.com")
    user2 = User("Leo Davis", "leo@example.com")
    storage.add_user(user1)
    storage.add_user(user2)
    loaded = storage.list_users()
    assert len(loaded) >= 2
    names = [u.name for u in loaded]
    assert "Kate Wilson" in names
    assert "Leo Davis" in names

def test_add_and_list_tasks(storage):
    user = User("Mia Taylor", "mia@example.com")
    storage.add_user(user)
    task = Task(user.user_id, "SQLite test", "Test SQLite persistence")
    storage.add_task(task)
    loaded = storage.list_tasks()
    assert any(t.title == "SQLite test" for t in loaded)

def test_generate_report(storage):
    users = storage.list_users()
    tasks = storage.list_tasks()
    assert storage.generate_report(tasks, users)
