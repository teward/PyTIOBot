#!/usr/bin/python3
# coding=utf-8

# noinspection PyUnresolvedReferences
from datetime import datetime
import os
from threading import Thread
import time
from globalvalues import GlobalValues

from chat_communicate import watcher

from excepthook import uncaught_exception, install_thread_excepthook
import sys
sys.excepthook = uncaught_exception
install_thread_excepthook()

se_rooms = {}
mse_rooms = {}
so_rooms = {}

# chat.stackexchange.com logon/wrapper
chatlogoncount = 0
for cl in range(1, 10):
    chatlogoncount += 1
    try:
        # chat.stackexchange.com
        GlobalValues.se_chat.login(GlobalValues.username, GlobalValues.password)

        # chat.meta.stackexchange.com
        GlobalValues.mse_chat.login(GlobalValues.username, GlobalValues.password)

        # chat.stackoverflow.com
        GlobalValues.so_chat.login(GlobalValues.username, GlobalValues.password)

        # If we didn't error out horribly, we can be done with this loop
        break

    except (ValueError, AssertionError):
        # One of the chats died, so let's wait a second, and start over.
        time.sleep(1)
        continue  # If we did error, we need to try this again.

# Handle "too many logon attempts" case to prevent infinite looping and to handle the 'too many logons' error.
if chatlogoncount >= 10:
    raise RuntimeError("Could not get at least one of the chat logons.")

# There is a master bot room at https://chat.stackexchange.com/rooms/68356/tiobot-python-fork-development
# and this is an always-join channel if we have SE Chat enabled.
se_botmaster_room = GlobalValues.se_chat.get_room(str(GlobalValues.se_botmaster_room_id))
se_botmaster_room.join()
se_botmaster_room.send_message('PyTIOBot is online, running on Lunar Eclipse.')

if GlobalValues.se_autojoins:
    # But we also have another set of functions to handle other things so blah.
    for id_ in GlobalValues.se_autojoins:
        se_rooms[id_] = GlobalValues.se_chat.get_room(str(id_))
        se_rooms[id_].join()
        se_rooms[id_].watch_socket(watcher)

if GlobalValues.mse_autojoins:
    for id_ in GlobalValues.mse_autojoins:
        mse_rooms[id_] = GlobalValues.mse_chat.get_room(str(id_))
        mse_rooms[id_].join()
        mse_rooms[id_].watch_socket(watcher)

if GlobalValues.so_autojoins:
    for id_ in GlobalValues.so_autojoins:
        so_rooms[id_] = GlobalValues.so_chat.get_room(str(id_))
        so_rooms[id_].join()
        so_rooms[id_].watch_socket(watcher)


# noinspection PyProtectedMember
def restart_automatically(time_in_seconds):
    time.sleep(time_in_seconds)
    exit(1)


Thread(name="auto restart thread", target=restart_automatically, args=(21600,)).start()

