# Task Management System

A professional Python task management system demonstrating Object-Oriented Programming, data persistence, and advanced Python concepts.

## Features

- **User Management**: Create and manage users with unique identifiers
- **Task Management**: Create tasks with status tracking (Pending, In Progress, Completed)
- **Data Persistence**: Save and load data in multiple formats (JSON, Pickle, CSV)
- **Task Filtering**: Filter tasks by status or user
- **Text Reports**: Generate human-readable reports of all tasks and users
- **Advanced Python**: Generators, iterators, and Pythonic patterns

## Project Structure

```
src/
├── models/              # Data models (User, Task)
│   ├── user.py         # User class definition
│   ├── task.py         # Task class and TaskStatus enum
│   └── __init__.py     # Package exports
├── core/               # Core business logic
│   ├── task_manager.py # TaskManager class for operations
│   └── __init__.py     # Package exports
└── storage/            # Data persistence layer
    ├── data_store.py   # DataStore class for I/O operations
    └── __init__.py     # Package exports

demo.py                 # Basic feature demonstration
advanced_example.py     # Advanced concepts showcase
test_system.py          # Unit tests
requirements.txt        # Project dependencies
.gitignore             # Git ignore patterns
```

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Demo

Run the basic demonstration:
```bash
python demo.py
```

### Advanced Examples

See generators, iterators, and advanced Python concepts:
```bash
python advanced_example.py
```

### Run Tests

Execute all unit tests:
```bash
python -m unittest test_system.py -v
```

Or run a specific test class:
```bash
python -m unittest test_system.py.TestTask -v
```

## API Overview

### TaskManager

```python
manager = TaskManager()

# User operations
user = manager.add_user("John Doe", "john@example.com")
users = manager.users

# Task operations
task = manager.add_task(user.user_id, "Title", "Description")
tasks = manager.get_user_tasks(user.user_id)
manager.update_task_status(user.user_id, task.task_id, TaskStatus.COMPLETED)
manager.delete_task(user.user_id, task.task_id)

# Filtering
completed_tasks = manager.filter_tasks_by_status(TaskStatus.COMPLETED)
```

### DataStore

```python
storage = DataStore()

# Save operations
storage.save_users_json(users, "users.json")
storage.save_tasks_pickle(tasks, "tasks.pkl")
storage.save_tasks_csv(tasks, "tasks.csv")

# Load operations
users = storage.load_users_json("users.json")
tasks = storage.load_tasks_pickle("tasks.pkl")

# Report generation
report = storage.generate_text_report(users, tasks)
```

### Models

```python
from src.models import User, Task, TaskStatus

# Create user
user = User("Alice", "alice@example.com")

# Create task
task = Task(user.user_id, "Important Task", "Task description")
task.status = TaskStatus.IN_PROGRESS

# Access properties
print(task.user_id, task.title, task.status.value)
```

## Key Concepts Demonstrated

- **Object-Oriented Programming**: Classes, encapsulation, methods
- **Data Persistence**: JSON, Pickle, and CSV formats
- **Generators**: Efficient iteration over large datasets
- **Custom Iterators**: Implementing `__iter__` and `__next__`
- **String Methods**: Manipulation and formatting
- **List Operations**: Comprehensions, filtering, sorting
- **Datetime**: Creating and comparing timestamps
- **Unit Testing**: Test organization with unittest framework
- **Package Structure**: Modular organization with `__init__.py`

## Testing

The project includes 11+ comprehensive unit tests covering:

- User creation and serialization
- Task creation and status updates
- TaskManager CRUD operations
- Task filtering by status
- DataStore persistence operations
- Report generation

All tests pass successfully:
```bash
python -m unittest test_system.py -v
```

## Dependencies

- Python 3.7+
- No external dependencies required for core functionality
- Optional: tabulate and colorama for enhanced output

## License

This project is created for academic purposes.

## Author

Jheison Martinez Bolivar
