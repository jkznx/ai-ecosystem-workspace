from backend.utils.labelstudio_client import get_client

for p in get_client().projects.list():
    print(f"id={p.id} title={p.title!r} task_number={p.task_number}")