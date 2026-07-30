from fastapi import APIRouter, Depends
from backend.api.deps import get_current_user
from backend.core.db.models import User
from backend.utils.labelstudio_client import get_client

router = APIRouter(prefix="/annotation", tags=["annotation"])

@router.get("/projects")
def list_projects(user: User = Depends(get_current_user)) -> list[dict]:
    client = get_client()
    return [{"id": p.id, "title": p.title, "task_number": p.task_number} for p in client.projects.list()]

@router.get("/projects/{project_id}/tasks")
def list_tasks(project_id: int, user: User = Depends(get_current_user)) -> list[dict]:
    client = get_client()
    return [{"id": t.id, "data": t.data} for t in client.tasks.list(project=project_id)]

@router.post("/projects/{project_id}/tasks", status_code=201)
def create_task(project_id: int, data: dict, user: User = Depends(get_current_user)) -> dict:
    client = get_client()
    task = client.tasks.create(project=project_id, data=data)
    return {"id": task.id, "data": task.data}

@router.get("/projects/{project_id}/export")
def export_project(project_id: int, export_type: str = "JSON", user: User = Depends(get_current_user)):
    client = get_client()
    export_result = client.projects.exports.create(id=project_id)
    return client.projects.exports.download(id=project_id, export_pk=export_result.id, export_type=export_type)