from src.apps.logging_.models import SystemInfo


def create_system_info_model(**kwargs) -> SystemInfo:
    return SystemInfo(**kwargs).save()
