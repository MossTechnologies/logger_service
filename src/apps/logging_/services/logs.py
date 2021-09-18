import json

from mongoengine.errors import DoesNotExist
from typing import Optional

from src.apps.logging_ import models
from src.apps.logging_.services.related_to_json import (
    related_system_info_to_json
)


class Logs:
    def __init__(
        self, 
        project_model: models.Project, 
        system_info_model: Optional[models.SystemInfo] = None
    ):
        self.project_model = project_model
        self.system_info_model = system_info_model

    def write(self, log: dict) -> None:
        models.Log(
            id_=self.generate_id_for_log(),
            log=log['log'],
            project=self.project_model,
            system_info=self.system_info_model
        ).save()

    def delete_log(self, log_id: int) -> bool:
        try:
            models.Log.objects.get(
                id_=log_id,
                project=self.project_model
            ).delete()

            return True
        except DoesNotExist:
            return False

    def delete_logs_for_project(self):
        models.Log.objects(
            project=self.project_model
        ).delete()

    def generate_id_for_log(self):
        return models.Log.objects.filter(project=self.project_model).count()


class LogsBrowser:
    def __init__(self, project_model):
        self.project_model = project_model

    def paginator(self, number_of_logs: int, step: int) -> list:
        offset = number_of_logs * (step - 1)
        
        logs = models.Log.objects(
            project=self.project_model
        ).skip(offset).limit(number_of_logs)

        offset_logs = json.loads(logs.to_json())
        
        related_system_info_to_json(logs, offset_logs)

        return offset_logs
