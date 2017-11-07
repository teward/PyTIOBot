# coding=utf-8
import json
# noinspection PyCompatibility
import urllib.request
# noinspection PyCompatibility
import urllib.parse
# noinspection PyCompatibility
import urllib.error
import zlib

from Tio import TioRequest, TioResponse
from typing import Union

class Tio:
    backend = "cgi-bin/run/api/"
    json = "languages.json"

    def __init__(self, url="https://tio.run"):
        self.backend = urllib.parse.urlparse(url + '/' + self.backend)
        self.json = urllib.parse.urlparse(url + '/' + self.json)

        raise NotImplementedError

    @staticmethod
    def read_in_chunks(stream_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = stream_object.read(chunk_size)
            if not data:
                break
            yield data

    @staticmethod
    def new_request():
        return TioRequest

    @staticmethod
    def query_languages(self):
        try:
            response = urllib.request.urlopen(urllib.request.Request(json))
            rawdata = json.loads(response.read().decode('utf-8'))
            data = rawdata.keys()
            return set(data)
        except (urllib.error.HTTPError, urllib.error.URLError):
            return set()
        except Exception:
            return set()

    def send(self, fmt: TioRequest):
        return self.send_bytes(fmt.as_bytes())

    def send_bytes(self, message: bytes):
        try:
            req = urllib.request.urlopen(self.backend, data=message)
            reqcode = req.getcode()
            if req.code == 200:
                fulldata = ''
                for data in self.read_in_chunks(req):
                    fulldata += req.read(1024).decode('utf-8')

                return TioResponse(reqcode, fulldata, None)
            else:
                return TioResponse(reqcode, None, None)
        except Exception as e:
            return TioResponse(-1, None, e)

    def prepare(self, response: Union[bytes, bytearray]):
        raise NotImplementedError
