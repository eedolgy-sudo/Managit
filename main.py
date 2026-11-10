import uvicorn
from fastapi import FastAPI, HTTPException
from schemas import TaskCreate, TaskRead, TaskUpdate#, User, Notification
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from database_crud import (delete_data, select_tasks, select_task, add_data,
                           update_data)
from database_models import TaskDB

app = FastAPI()

global_temp_list = []

FRONTEND = Path(__file__).resolve().parent / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND),
    name="static"
)


@app.get("/tasks", response_model=list[TaskRead])
async def get_tasks():
    return select_tasks()


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = select_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.post("/tasks")
async def create_task(task: TaskCreate):
    new_task = TaskDB(**task.model_dump())
    add_data([new_task])
    return 'Task ' + task.name + ' created successfully'


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    changes = task.model_dump(exclude_unset=True)
    updated = update_data(TaskDB, task_id, changes)

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated successfully"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = delete_data(TaskDB, task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)