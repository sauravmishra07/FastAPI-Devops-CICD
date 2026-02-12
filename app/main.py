import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from typing import List

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

APP_NAME = os.getenv("APP_NAME", "FastAPI Todo App")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# In-memory todo list
todos: List[dict] = []
 

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos,
        "app_name": APP_NAME,
        "app_version": APP_VERSION
    })


@app.post("/add")
def add_todo(title: str = Form(...)):
    todos.append({"id": len(todos) + 1, "title": title})
    return RedirectResponse("/", status_code=303)


@app.post("/delete/{todo_id}")
def delete_todo(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return RedirectResponse("/", status_code=303)
