# coding=utf-8

import traceback
from datetime import datetime
from helpers import log


def log_exception(exctype, value, tb):
    now = datetime.utcnow()
    tr = '\n'.join((traceback.format_tb(tb)))
    exception_only = ''.join(traceback.format_exception_only(exctype, value)).strip()
    logged_msg = "{exception}\n{now} UTC\n{row}\n\n".format(exception=exception_only, now=now, row=tr)
    log('error', logged_msg)
    with open("errorLogs.txt", "a") as f:
        f.write(logged_msg)
