from mongoengine.errors import DoesNotExist

from src.apps.logging_ import models
from src.services.db import generate_id_for_any_model

import json


class Project:
    def __init__(self, client_name: str, project_name: str = None):
        self.client_name = client_name
        self.project_name = project_name

    def get_or_create_project(self) -> models.Project:
        """
            If project for current client_name exists - get.
            If project for current client_name does not exists - create and get.
        """

        if models.Project.objects.filter(
            client_name=self.client_name,
            name=self.project_name
        ).count() > 0:
            return models.Project.objects.get(
                client_name=self.client_name,
                name=self.project_name
            )
        return models.Project(
            id_=generate_id_for_any_model(model=models.Project),
            client_name=self.client_name,
            name=self.project_name
        ).save()

    def delete(self) -> bool:
        """ Delete project for current token. """

        try:
            # Delete all logs for current project
            models.Log.objects(
                project=models.Project.objects.get(
                    client_name=self.client_name,
                    name=self.project_name
                )
            ).delete()

            models.Project.objects.get(
                client_name=self.client_name,
                name=self.project_name
            ).delete()

            return True  # if deleted
        except DoesNotExist:
            return False  # if not deleted

    def get_projects(self) -> list[dict]:
        """ Get all projects for current token. """

        return json.loads(
            models.Project.objects.filter(
                client_name=self.client_name
            ).to_json()
        )
