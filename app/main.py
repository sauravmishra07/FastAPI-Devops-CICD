import os
import json
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from typing import List

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "FastAPI Todo App")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="""
## 📝 FastAPI Todo Application

This is a simple Todo application built with FastAPI.

### Features:
- Add todos
- Edit todos
- Delete todos
- Toggle completion
- Clear completed tasks
- File-based persistence (JSON)

Visit:
- `/docs` → Swagger UI
- `/redoc` → ReDoc Documentation
""",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

templates = Jinja2Templates(directory="app/templates")

# Data file for simple persistence
DATA_FILE = Path("app/todos.json")


def load_todos() -> List[dict]:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_todos(todos: List[dict]):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(todos, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


# In-memory (backed by file) todo list
todos: List[dict] = load_todos()


def next_id() -> int:
    if not todos:
        return 1
    return max(todo.get("id", 0) for todo in todos) + 1


@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos,
        "app_name": APP_NAME,
        "app_version": APP_VERSION
    })


@app.post("/add", tags=["Todos"])
def add_todo(title: str = Form(...)):
    todo = {
        "id": next_id(),
        "title": title,
        "completed": False,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    todos.append(todo)
    save_todos(todos)
    return RedirectResponse("/", status_code=303)


@app.post("/delete/{todo_id}", tags=["Todos"])
def delete_todo(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo.get("id") != todo_id]
    save_todos(todos)
    return RedirectResponse("/", status_code=303)


@app.post("/toggle/{todo_id}", tags=["Todos"])
def toggle_todo(todo_id: int):
    for todo in todos:
        if todo.get("id") == todo_id:
            todo["completed"] = not todo.get("completed", False)
            break
    save_todos(todos)
    return RedirectResponse("/", status_code=303)


@app.post("/edit/{todo_id}", tags=["Todos"])
def edit_todo(todo_id: int, title: str = Form(...)):
    for todo in todos:
        if todo.get("id") == todo_id:
            todo["title"] = title
            break
    save_todos(todos)
    return RedirectResponse("/", status_code=303)


@app.post("/clear_completed", tags=["Todos"])
def clear_completed():
    global todos
    todos = [todo for todo in todos if not todo.get("completed", False)]
    save_todos(todos)
    return RedirectResponse("/", status_code=303)
