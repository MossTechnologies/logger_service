from starlette.config import Config


config = Config()

# app configurations
DEBUG = config("DEBUG", cast=bool, default=True)

PROJECT_NAME = 'FastAPI Log handling Service'
PROJECT_DESCRIPTION = 'Author - IllyaMoss <illya08mosiychuk@gmail.com>'
PROJECT_VERSION = '0.2.8'

# mongo configurations
MONGODB_HOST = config('MONGODB_HOST', cast=str, default='127.0.0.1')
MONGODB_PORT = config('MONGODB_PORT', cast=int, default=27017)
MONGODB_DATABASE = config('MONGODB_DATABASE', cast=str, default="LogDB")
MONGODB_USER = config('MONGODB_USER', cast=str, default="root")
MONGODB_PASSWORD = config('MONGODB_PASSWORD', cast=str, default="MongoDBRootPassword_cyferka2")

# JWT
SECRET_KEY = config(
    'SECRET_KEY_JWT',
    cast=str,
    default='c83300e0d44f78bbcfe119439603c5953e2bcaf1deb03538840ab962d00ff5bd'
)
ALGORITHM_JWT = config('ALGORITHM_JWT', cast=str, default='HS256')
