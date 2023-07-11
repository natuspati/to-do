from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "ToDo"
VERSION = "1.0.0"
API_PREFIX = "/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret)

DATABASE_URL = config(
    "DATABASE_URL",
)
DATABASE_NAME = config(
    "DATABASE_NAME",
)
