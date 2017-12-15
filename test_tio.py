#!/usr/bin/python3
# coding=utf-8
from pytio import Tio, TioRequest

tio = Tio()

request = TioRequest(lang='apl-dyalog', code="")

# request.set_lang(input("Lang: "))
# request.set_code(input("Code: "))

data = tio.send(request)

print(data.raw.decode('utf-8').split('\r\n'))

if data.error:
    print("ERROR: {}".format(data.error))
else:
    print("RESULT: {}".format(data.result))
