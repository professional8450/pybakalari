from __future__ import annotations

from typing import Any, Dict, Union


class BakalariException(Exception):
    def __init__(self, message: Union[Dict[str, Any], str]):
        if isinstance(message, dict):
            error = message.get('error_description', message.get('Message', None))
            super().__init__(error)
        else:
            super().__init__(message)


class BadRequest(BakalariException):
    def __init__(self, message: Union[Dict[str, Any], str]):
        super().__init__(message)


class NotFound(BakalariException):
    def __init__(self, message: Union[Dict[str, Any], str]):
        super().__init__(message)


class InvalidServerResponse(BakalariException):
    def __init__(self, message: Union[Dict[str, Any], str]):
        super().__init__(message)


class Unauthorized(BakalariException):
    def __init__(self, message: Union[Dict[str, Any], str]):
        super().__init__(message)
