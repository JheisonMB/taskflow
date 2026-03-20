#!/usr/bin/env python3

import unittest
from datetime import datetime
from src.models import User, Task, TaskStatus
from src.core import TaskManager
from src.storage import DataStore
import json
import os


class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User("John Doe", "john@example.com")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertIsNotNone(user.user_id)

    def test_user_to_dict(self):
        user = User("Jane Smith", "jane@example.com")
        user_dict = user.to_dict()
        self.assertIn("user_id", user_dict)
        self.assertIn("name", user_dict)
        self.assertIn("email", user_dict)
        self.assertEqual(user_dict["name"], "Jane Smith")


class TestTask(unittest.TestCase):
    def test_task_creation(self):
        task = Task("user123", "Complete project", "Finish the final deliverable")
        self.assertEqual(task.title, "Complete project")
        self.assertEqual(task.description, "Finish the final deliverable")
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertIsNotNone(task.task_id)

    def test_task_status_change(self):
        task = Task("user123", "Review code", "Review PR #42")
        self.assertEqual(task.status, TaskStatus.PENDING)
        task.status = TaskStatus.IN_PROGRESS
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
        task.status = TaskStatus.COMPLETED
        self.assertEqual(task.status, TaskStatus.COMPLETED)

    def test_task_to_dict(self):
        task = Task("user456", "Write docs", "Add API documentation")
        task_dict = task.to_dict()
        self.assertIn("task_id", task_dict)
        self.assertIn("user_id", task_dict)
        self.assertIn("title", task_dict)
        self.assertIn("status", task_dict)
        self.assertEqual(task_dict["user_id"], "user456")


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()

    def test_add_user(self):
        user = self.manager.add_user("Alice Wonder", "alice@example.com")
        self.assertEqual(user.name, "Alice Wonder")
        self.assertEqual(len(self.manager.users), 1)

    def test_add_multiple_users(self):
        user1 = self.manager.add_user("Bob Builder", "bob@example.com")
        user2 = self.manager.add_user("Carol Davis", "carol@example.com")
        self.assertEqual(len(self.manager.users), 2)
        self.assertNotEqual(user1.user_id, user2.user_id)

    def test_add_task(self):
        user = self.manager.add_user("David Lee", "david@example.com")
        task = self.manager.add_task(user.user_id, "Test task", "Description here")
        self.assertEqual(task.user_id, user.user_id)
        self.assertEqual(len(self.manager.tasks), 1)

    def test_get_user_tasks(self):
        user = self.manager.add_user("Eve Miller", "eve@example.com")
        task1 = self.manager.add_task(user.user_id, "Task 1", "First task")
        task2 = self.manager.add_task(user.user_id, "Task 2", "Second task")
        user_tasks = self.manager.get_user_tasks(user.user_id)
        self.assertEqual(len(user_tasks), 2)

    def test_update_task_status(self):
        user = self.manager.add_user("Frank Wilson", "frank@example.com")
        task = self.manager.add_task(
            user.user_id, "Status test", "Test updating status"
        )
        self.manager.update_task_status(
            user.user_id, task.task_id, TaskStatus.IN_PROGRESS
        )
        updated_task = self.manager.get_task(user.user_id, task.task_id)
        self.assertEqual(updated_task.status, TaskStatus.IN_PROGRESS)

    def test_filter_tasks_by_status(self):
        user1 = self.manager.add_user("Grace Lee", "grace@example.com")
        user2 = self.manager.add_user("Henry Brown", "henry@example.com")
        task1 = self.manager.add_task(user1.user_id, "Completed task", "Done")
        task2 = self.manager.add_task(user2.user_id, "Pending task", "Not started")
        self.manager.update_task_status(
            user1.user_id, task1.task_id, TaskStatus.COMPLETED
        )

        completed_tasks = self.manager.filter_tasks_by_status(TaskStatus.COMPLETED)
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].task_id, task1.task_id)

    def test_delete_task(self):
        user = self.manager.add_user("Iris White", "iris@example.com")
        task = self.manager.add_task(
            user.user_id, "To delete", "This task will be deleted"
        )
        self.assertEqual(len(self.manager.tasks), 1)
        self.manager.delete_task(user.user_id, task.task_id)
        self.assertEqual(len(self.manager.tasks), 0)

    def test_get_task(self):
        user = self.manager.add_user("Jack Martin", "jack@example.com")
        task = self.manager.add_task(user.user_id, "Find me", "Retrieve this task")
        retrieved = self.manager.get_task(user.user_id, task.task_id)
        self.assertEqual(retrieved.task_id, task.task_id)
        self.assertEqual(retrieved.title, "Find me")


class TestDataStore(unittest.TestCase):
    def setUp(self):
        self.storage = DataStore()
        self.manager = TaskManager()
        self.cleanup_files()

    def tearDown(self):
        self.cleanup_files()

    def cleanup_files(self):
        for filename in [
            "test_users.json",
            "test_tasks.pkl",
            "test_tasks.csv",
            "test_report.txt",
        ]:
            if os.path.exists(filename):
                os.remove(filename)

    def test_save_and_load_users_json(self):
        user1 = self.manager.add_user("Kate Wilson", "kate@example.com")
        user2 = self.manager.add_user("Leo Davis", "leo@example.com")

        self.storage.save_users_json(self.manager.users, "test_users.json")
        loaded = self.storage.load_users_json("test_users.json")

        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].name, "Kate Wilson")

    def test_save_and_load_tasks_pickle(self):
        user = self.manager.add_user("Mia Taylor", "mia@example.com")
        task = self.manager.add_task(user.user_id, "Pickle test", "Test pickling")

        self.storage.save_tasks_pickle(self.manager.tasks, "test_tasks.pkl")
        loaded = self.storage.load_tasks_pickle("test_tasks.pkl")

        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].title, "Pickle test")

    def test_generate_text_report(self):
        user1 = self.manager.add_user("Noah Harris", "noah@example.com")
        user2 = self.manager.add_user("Olivia Clark", "olivia@example.com")
        task1 = self.manager.add_task(user1.user_id, "Task A", "Description A")
        task2 = self.manager.add_task(user2.user_id, "Task B", "Description B")

        report = self.storage.generate_text_report(
            self.manager.users, self.manager.tasks
        )

        self.assertIn("Noah Harris", report)
        self.assertIn("Task A", report)
        self.assertIn("Task B", report)


if __name__ == "__main__":
    unittest.main()
