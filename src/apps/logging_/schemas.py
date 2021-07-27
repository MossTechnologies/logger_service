from pydantic import BaseModel
from typing import Union


class Log(BaseModel):
    level: str
    level_number: int
    func_name: str
    path_to_file: str
    line: int
    message: str
    created: str
    additional_info: dict[Union[str, int], Union[str, int]]


class Logging(BaseModel):
    project_name: str
    log: Log
