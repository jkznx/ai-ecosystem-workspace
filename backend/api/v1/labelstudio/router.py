from fastapi import APIRouter, Depends

from backend.api.deps import get_current_user
from backend.api.schemas.labelstudio import LabelStudioProject, LabelStudioTask, TaskCreateRequest
from backend.core.db.models import User
from backend.services.annotation_service import annotation_service

router = APIRouter(prefix="/labelstudio", tags=["labelstudio"])


# ---- load: read only ----
@router.get("/load/projects", response_model=list[LabelStudioProject])
def load_projects(user: User = Depends(get_current_user)) -> list[LabelStudioProject]:
    return annotation_service.list_projects()


@router.get("/load/tasks/{project_id}", response_model=list[LabelStudioTask])
def load_tasks(project_id: int, user: User = Depends(get_current_user)) -> list[LabelStudioTask]:
    return annotation_service.list_tasks(project_id)


@router.get("/load/export/{project_id}")
def load_export(project_id: int, export_type: str = "JSON", user: User = Depends(get_current_user)):
    return annotation_service.export(project_id, export_type)


# ---- store: write/update ----
@router.post("/store/tasks/{project_id}", response_model=LabelStudioTask, status_code=201)
def store_task(
    project_id: int, body: TaskCreateRequest, user: User = Depends(get_current_user)
) -> LabelStudioTask:
    return annotation_service.create_task(project_id, body.data)
