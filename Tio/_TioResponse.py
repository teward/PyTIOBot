# coding=utf-8

from typing import Optional, Any


class TioResponse:
    _code = 0
    _result = None
    _error = None

    def __init__(self, code, result: Optional[Any] = None, error: Optional[Any] = None):
        self._code = code
        self._result = result
        self._error = error

    @property
    def code(self):
        return self._code

    @property
    def result(self):
        return self._result

    @property
    def error(self):
        return self._error

    def get_code(self):
        return self.code

    def get_result(self):
        return self.result

    def get_error(self):
        return self.error
