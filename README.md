# Sistema de Gestión de Tareas

Este es un proyecto académico hecho en Python para gestionar tareas y usuarios en una empresa de software.

## Diagramas de diseño

### Casos de Uso
```mermaid
sequenceDiagram
    autonumber
    actor U as Usuario
    participant S@{ "type": "boundary" } as Sistema
    participant DB@{ "type" : "database" } as SQLite

    U->>S: Crear tarea
    S->>DB: Insertar tarea
    DB-->>S: Confirmación
    S-->>U: Tarea creada

```

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuario
    participant S@{ "type": "boundary" } as Sistema
    participant DB@{ "type" : "database" } as SQLite

    U->>S: Consultar tareas
    S->>DB: Leer tareas
    DB-->>S: Lista de tareas
    S-->>U: Mostrar tareas
```

---


### Entidades

```mermaid
erDiagram
    USUARIO {
        int id PK
        string nombre
        string email
    }
    TAREA {
        int id PK
        string titulo
        string descripcion
        date fecha_creacion
        date fecha_limite
        string estado
        int usuario_id FK
     }
    USUARIO ||--o{ TAREA : asigna
```

---


### Solución
```mermaid
classDiagram
    class User {
        +str user_id
        +str name
        +str email
        +list assigned_tasks
        +add_task(task_id)
        +remove_task(task_id)
        +get_tasks()
        +to_dict()
        +from_dict(data)
    }
    class Task {
        +str task_id
        +str user_id
        +str title
        +str description
        +str assignee
        +datetime created_at
        +datetime due_date
        +TaskStatus status
        +datetime completed_at
        +set_status(status)
        +reassign(new_assignee)
        +days_until_due()
        +is_overdue()
        +to_dict()
        +from_dict(data)
    }
    class TaskStatus {
        <<enumeration>>
        PENDING
        IN_PROGRESS
        COMPLETED
    }
    class TaskManager {
        +dict users
        +dict tasks
        +add_user(name, email)
        +get_user(user_id)
        +list_users()
        +add_task(assignee, title, description, due_date)
        +get_task(user_id, task_id)
        +list_tasks()
        +delete_task(user_id, task_id)
        +update_task_status(user_id, task_id, status)
        +filter_tasks_by_status(status)
        +get_user_tasks(user_id)
        +filter_by_assignee(user_id)
        +get_overdue_tasks()
        +get_upcoming_tasks(days)
        +iter_user_tasks(user_id)
        +iter_all_tasks()
        +iter_users()
        +get_stats()
        +get_user_stats(user_id)
    }
    User "1" -- "0..*" Task : asigna
    TaskManager o-- User
    TaskManager o-- Task
    Task o-- TaskStatus
```

## ¿Cómo lo uso?

1. **Crea un entorno virtual (recomendado):**

```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

3. **Ejecuta la demo básica:**

```bash
python3 demo.py
```

Esto crea usuarios, tareas, actualiza estados y guarda los datos.

4. **Ejecuta el ejemplo avanzado:**

```bash
python3 advanced_example.py
```

Aquí verás generadores, iteradores y más cosas de Python.

5. **Corre las pruebas (recomendado):**

```bash
pytest
```
