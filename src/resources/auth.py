from functools import wraps

from flask import request
from flask_restful import abort

from src.api.auth import AuthAPI


def requires_auth(schemes=("basic",)):
    """Validate endpoint against given authorization schemes.
    Fail if authorization properties are missing or are invalid."""

    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if "basic" in schemes:
                auth = request.authorization
                if auth and AuthAPI.authenticate(
                        username=auth.username,
                        password=auth.password
                ):
                    return func(*args, **kwargs)
            elif "bearer" in schemes:
                raise NotImplementedError

            abort(401, code=401, reason="Unauthorized")

        return decorated

    return wrapper
