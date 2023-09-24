# Taskonomics: Where Tasks Mean Business

## Installation

```shell
# Activate virtual environment
poetry shell

# Install dependencies
poetry install

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

or

```shell
# Deploy to Fly.io
fly deploy
```

## API Routes

All routes are prefixed with `/api/v1/`

- Authentication
    - POST `signup/` (create user)
    - POST `login/` (get access token)
    - POST `login/refresh/` (refresh access token)
- Tasks
    - GET `task/` (list tasks)
    - POST `task/` (create task)
    - GET `task/<int:pk>/` (retrieve task)
    - PUT `task/<int:pk>/` (update task)
    - DELETE `task/<int:pk>/` (delete task)
- Projects
    - GET `project/` (list projects)
    - POST `project/` (create project)
    - GET `project/<int:pk>/` (retrieve project)
    - PUT `project/<int:pk>/` (update project)
    - DELETE `project/<int:pk>/` (delete project)

## How do timestamps work?

The timestamps are stored in UTC time. When a user creates a task, the timestamp is converted to UTC time and stored in
the database. When a user views a task, the timestamp is converted to the user's local time and displayed, we do this by
fetching the user's timezone in the database.
