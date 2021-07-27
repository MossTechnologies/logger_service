from fastapi import APIRouter, Request, Security, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

from src.apps.logging_.services.logs import LogsBrowser, Logs
from src.apps.logging_.services.projects import Project
from src.apps.logging_.schemas import Logging

from src.services import token

from mongoengine.errors import DoesNotExist


router = APIRouter()
security = HTTPBearer()


@router.post('/write/', tags=['frontend_logging_api', 'user_logging_api'])
async def write_log(
    logging: Logging,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> JSONResponse:
    """ Get log from client and write log to data base. """
    client_name = token.decode_token(credentials.credentials)['sub']

    if 'content-type' not in request.headers:
        return JSONResponse({
            'detail': 'In request must be content-type'
        }, status_code=400)

    if request.headers['content-type'].lower() == 'application/json':
        try:
            project_model = Project(
                client_name,
                logging.project_name
            ).get_or_create_project()
            Logs(project_model).write(log=logging.dict())

            return JSONResponse({'detail': 'Log successful created'}, status_code=201)
        except DoesNotExist:
            return JSONResponse({'detail': 'Token not found!'}, status_code=404)

    else:
        return JSONResponse({
            'detail': 'Not the correct content type, it must be '
                      '"application/x-www-form-urlencoded" or "application/json"'
        }, status_code=400)


@router.get(
    '/logs-paginator/{project_name}/{number_of_logs}/{step}',
    tags=['frontend_logging_api']
)
async def logs_paginator(
    project_name: str,
    number_of_logs: int,
    step: int,
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> JSONResponse:
    try:
        client_name = token.decode_token(credentials.credentials)['sub']

        project_model = Project(client_name, project_name).get_or_create_project()

        return JSONResponse({
            'project_name': project_name,
            'logs': LogsBrowser(project_model).paginator(number_of_logs, step),
        }, status_code=200)
    except DoesNotExist:
        return JSONResponse({
            'detail': 'No logs have been received for this name yet'
        }, status_code=404)


@router.delete(
    '/delete-current-log/{project_name}/{log_id}',
    tags=['frontend_logging_api', 'user_logging_api']
)
async def delete_current_log(
    project_name: str,
    log_id: int,
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Response:
    client_name = token.decode_token(credentials.credentials)['sub']

    project_model = Project(client_name, project_name).get_or_create_project()

    deleted = Logs(project_model).delete_log(log_id)

    if not deleted:
        return JSONResponse({
            'detail': f'Log with ID: {log_id}, '
                      f'PROJECT NAME: {project_name} does not exists!'
        }, status_code=404)

    return Response(status_code=204)


@router.get('/get-all-projects/', tags=['frontend_logging_api'])
async def get_all_projects_for_current_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> JSONResponse:
    client_name = token.decode_token(credentials.credentials)['sub']
    return JSONResponse({'projects': Project(client_name).get_projects()}, status_code=200)


@router.delete(
    '/delete-current-project/{project_name}',
    tags=['frontend_logging_api']
)
async def delete_current_project(
    project_name: str,
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Response:
    client_name = token.decode_token(credentials.credentials)['sub']

    deleted = Project(client_name, project_name).delete()

    if not deleted:
        return JSONResponse({
            'detail': f'Logger with NAME: {project_name} does not exists!'
        }, status_code=404)

    return Response(status_code=204)
