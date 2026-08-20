import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional
from contextlib import asynccontextmanager


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    done: bool = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Tasks API", version="1.0.0", lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/tasks", response_model=Task)
def create_task(task: Task, session: Session = Depends(get_session)):
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.get("/tasks", response_model=list[Task])
def list_tasks(session: Session = Depends(get_session)):
        tasks = session.exec(select(Task)).all()
        return tasks

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
        return {"message": "Task deleted"}