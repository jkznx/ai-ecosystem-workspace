from label_studio_sdk import LabelStudio
from backend.core.config import settings


def get_client() -> LabelStudio:
    return LabelStudio(base_url=settings.LABEL_STUDIO_URL, api_key=settings.LABEL_STUDIO_API_KEY)