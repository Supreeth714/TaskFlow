# TaskFlow - Django Task Management

Full-stack task manager built with Django + DRF + Channels (WebSockets).

## Features
- Custom User model with registration & login (session + JWT)
- CRUD for tasks (title, description, status, priority, due date)
- Per-user task isolation (you only see your own tasks)
- Search & filter by status
- Responsive Bootstrap 5 UI (works on mobile & desktop)
- REST API at `/api/tasks/` (JWT auth)
- Real-time updates via WebSockets (`/ws/tasks/`)

## Setup

```bash
python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations accounts tasks
python manage.py migrate
python manage.py createsuperuser
# Dev server (HTTP only):
python manage.py runserver
# For WebSocket support, run via Daphne (ASGI):
daphne -b 0.0.0.0 -p 8000 taskproject.asgi:application
```

Open http://localhost:8000

## REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Create user `{username,email,password}` |
| POST | /api/auth/token/ | Obtain JWT `{username,password}` |
| POST | /api/auth/token/refresh/ | Refresh JWT |
| GET/POST | /api/tasks/ | List / create tasks |
| GET/PUT/PATCH/DELETE | /api/tasks/{id}/ | Retrieve / update / delete |

Include header: `Authorization: Bearer <access_token>`

## WebSocket
Connect to `ws://localhost:8000/ws/tasks/` (must be authenticated via session).
Receives `{action, task}` messages on create/update/delete.

## Project Structure
```
taskproject/   # Django settings, URLs, ASGI/WSGI
accounts/      # Custom User model + auth views/APIs
tasks/         # Task model, views, REST API, WebSocket consumer
templates/     # Bootstrap UI templates
static/        # CSS
```
