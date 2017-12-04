#!/usr/bin/python3
# coding=utf-8
from Tio import Tio, TioRequest

tio = Tio()
request = TioRequest(lang='apl-dyalog', code="⎕←'Hello, World!'")

# request.set_lang(input("Lang: "))
# request.set_code(input("Code: "))

print(request.as_bytes())

data = tio.send(request)

if data.error:
    print(data.error)
else:
    print(data.result)
