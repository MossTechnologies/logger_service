from mongoengine.errors import DoesNotExist

from src.apps.logging_ import models

import json


class Logs:
    def __init__(self, project_model):
        self.project_model = project_model

    def write(self, log: dict) -> None:
        print(self.generate_id_for_log())
        models.Log(
            id_=self.generate_id_for_log(),
            log=log['log'],
            project=self.project_model
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

    def generate_id_for_log(self):
        return models.Log.objects.filter(project=self.project_model).count()


class LogsBrowser:
    def __init__(self, project_model):
        self.project_model = project_model

    def paginator(self, number_of_logs: int, step: int) -> list:
        offset = number_of_logs * (step - 1)

        logs = json.loads(
            models.Log.objects.filter(
                project=self.project_model
            ).to_json()
        )[offset:number_of_logs]

        return logs
