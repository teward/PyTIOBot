# coding=utf-8

import os
from globalvalues import GlobalValues
from collections import namedtuple
from datetime import datetime
from termcolor import colored


Response = namedtuple('Response', 'command_status message')


# Allows use of `environ_or_none("foo") or "default"` shorthand
# noinspection PyBroadException,PyMissingTypeHints
def environ_or_none(key):
    try:
        return os.environ[key]
    except:
        return None


# noinspection PyMissingTypeHints
def log(log_level, *args):
    colors = {
        'debug': 'grey',
        'info': 'cyan',
        'warning': 'yellow',
        'error': 'red'
    }
    color = (colors[log_level] if log_level in colors else 'white')
    log_str = u"{} {}".format(colored("[{}]".format(datetime.now().isoformat()[11:-7]), color),
                              u"  ".join([str(x) for x in args]))
    print(log_str)


# noinspection PyMissingTypeHints
def is_privileged(chat_site, user_id_str, wrap2):
    if user_id_str in GlobalValues.privileged_users[chat_site]:
        return True
    user = wrap2.get_user(user_id_str)
    return user.is_moderator
