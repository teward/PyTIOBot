# coding=utf-8

import sys
import zlib
from typing import List, AnyStr, Union
from Tio import TioFile, TioVariable


class TioRequest:
    _files = []
    _variables = []
    _bytes = bytes()

    def __init__(self):
        pass  # No special action.

    def add_file(self, file: TioFile):
        if file in self._files:
            self._files.remove(file)
        self._files.append(file)

    def add_file_bytes(self, name: AnyStr, content: bytes):
        self._files.append(TioFile(name, content))

    def add_variable(self, variable: TioVariable):
        if variable in self._variables:
            self._variables.remove(variable)
        self._variables.append(variable)

    def add_variable_string(self, name: AnyStr, value: Union[List[AnyStr], AnyStr]):
        self._variables.append(TioFile(name, value))

    def set_lang(self, lang: AnyStr):
        self.add_variable_string('lang', lang)

    def set_code(self, code: AnyStr):
        self.add_variable_string('.code.tio', code)

    def set_input(self, input_data: AnyStr):
        self.add_file_bytes('.input.tio', input_data.encode('utf-8'))

    def set_compiler_flags(self, flags: AnyStr):
        self.add_variable_string('TIO_CFLAGS', flags)

    def set_commandline_flags(self, flags: AnyStr):
        self.add_variable_string('TIO_OPTIONS', flags)

    def set_arguments(self, args: AnyStr):
        self.add_variable_string('args', args)

    def write_variable(self, name: AnyStr, values: List[AnyStr]):
        if values:
            self._bytes += str("V" + name).encode('utf-8') + b'0'
            for value in values:
                self._bytes += str(value).encode('utf-8') + b'0'

    def write_file(self, name: AnyStr, file: bytes):
        self._bytes += str("F" + name).encode('utf-8') + b'0'
        self._bytes += file

    def as_bytes(self):
        try:
            for var in self._variables:
                self.write_variable(var.name, var.content)

            for file in self._files:
                self.write_variable(file.name, file.content)

        except IOError:
            raise RuntimeError("IOError generated during bytes conversion.")

        if sys.version_info >= (3, 6):  # 'level' in compress only works in Py 3.6+
            deflated = zlib.compress(self._bytes, level=2)
        else:
            deflated = zlib.compress(self._bytes)

        return deflated
