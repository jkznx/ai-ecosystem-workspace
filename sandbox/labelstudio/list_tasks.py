import sys
from backend.utils.labelstudio_client import get_client

project_id = int(sys.argv[1])
for t in get_client().tasks.list(project=project_id):
    print(f"id={t.id} data={t.data}")