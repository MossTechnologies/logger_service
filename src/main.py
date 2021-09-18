from fastapi import FastAPI
from fastapi.security import HTTPBearer

from mongoengine import connect, disconnect

from src.core import config
from src.apps.routers import router


security = HTTPBearer()

app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version=config.PROJECT_VERSION,
    openapi_prefix='' if config.DEBUG else '/loggerService'
)


app.include_router(router, prefix='' if config.DEBUG else "/loggerService")


@app.on_event('startup')
def startup():
    """ Connect to db """
    if config.DEBUG:
        # Development
        return connect(
            config.MONGODB_DATABASE,
            alias='default',
            host=config.MONGODB_HOST,
            port=config.MONGODB_PORT,
        )
    else:
        # Production
        return connect(
            config.MONGODB_DATABASE,
            alias='default',
            host=config.MONGODB_HOST,
            port=config.MONGODB_PORT,
            username=config.MONGODB_USER,
            password=config.MONGODB_PASSWORD,
            authentication_source='admin'
        )


@app.on_event('shutdown')
def shutdown():
    """ Disconnect from db """
    return disconnect()
