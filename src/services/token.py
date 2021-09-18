import jwt

from fastapi import HTTPException
from typing import Union

from src.core.config import SECRET_KEY, ALGORITHM_JWT


def decode_token(token: str) -> dict[str, Union[str, int]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM_JWT)

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')
