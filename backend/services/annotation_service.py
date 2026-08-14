from typing import Any

from backend.libs.labelstudio_client import get_client


class AnnotationService:

    def list_projects(self) -> list[dict[str, Any]]:
        client = get_client()
        return [
            {"id": p.id, "title": p.title, "task_number": p.task_number}
            for p in client.projects.list()
        ]

    def list_tasks(self, project_id: int) -> list[dict[str, Any]]:
        client = get_client()
        return [{"id": t.id, "data": t.data} for t in client.tasks.list(project=project_id)]

    def create_task(self, project_id: int, data: dict[str, Any]) -> dict[str, Any]:
        client = get_client()
        task = client.tasks.create(project=project_id, data=data)
        return {"id": task.id, "data": task.data}

    def export(self, project_id: int, export_type: str = "JSON"):
        client = get_client()
        export_result = client.projects.exports.create(id=project_id)
        return client.projects.exports.download(
            id=project_id, export_pk=export_result.id, export_type=export_type
        )


annotation_service = AnnotationService()
