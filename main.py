from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Tasks API", version="1.0.0")

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    done: bool = False

tasks: list[Task] = []
next_id = 1

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    global next_id
    task.id = next_id
    next_id += 1
    tasks.append(task)
    return task

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return tasks

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    for t in tasks:
        if t.id == task_id:
            tasks = [t for t in tasks if t.id != task_id]
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

