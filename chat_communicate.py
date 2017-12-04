# coding=utf-8

import re
from globalvalues import GlobalValues
from termcolor import colored
from helpers import log, Response
from ChatExchange.chatexchange.messages import Message
from excepthook import log_exception
import sys
import requests
import chat_commands
import traceback
import os

cmds = chat_commands.command_dict


# noinspection PyMissingTypeHints
def print_chat_message(ev):
    message = colored("Chat message in " + ev.data["room_name"] + " (" + str(ev.data["room_id"]) + "): \"",
                      attrs=['bold'])
    message += ev.data['content']
    message += "\""
    log('info', message + colored(" - " + ev.data['user_name'], attrs=['bold']))


# noinspection PyMissingTypeHints,PyBroadException
def watcher(ev, wrap2):
    try:
        # print(ev)  # FOR DEBUGGING ONLY
        if ev.type_id != 1 and ev.data['user_id'] != GlobalValues.bot_user_id[wrap2.host]:
            return

        ev_room = str(ev.data["room_id"])
        ev_user_id = str(ev.data["user_id"])
        ev_room_name = ev.data["room_name"].encode('utf-8')
        ev.message = Message(ev.message.id, wrap2)
        content_source = ev.message.content_source
        message_id = ev.message.id

        print_chat_message(ev)

        message_parts = re.split('[ ,]+', content_source)

        ev_user_name = ev.data["user_name"]
        ev_user_link = "//chat.{host}/users/{user_id}".format(host=wrap2.host, user_id=ev.user.id)

        try:
            reply = ''
            result = handle_commands(content_lower=content_source.lower(),
                                     message_parts=message_parts,
                                     ev_room=ev_room,
                                     ev_room_name=ev_room_name,
                                     ev_user_id=ev_user_id,
                                     ev_user_name=ev_user_name,
                                     wrap2=wrap2,
                                     content=content_source,
                                     message_id=message_id)
            if not result:  # avoiding errors due to unprivileged commands
                result = Response(command_status=True, message=None)
            if result.command_status and result.message:
                reply += result.message + os.linesep
            if result.command_status is False:
                pass
            if result.message is None and result.command_status is not False:
                pass

            reply = reply.strip()
            if reply != "":
                message_with_reply = u":{} {}".format(message_id, reply)
                if len(message_with_reply) <= 500 or "\n" in reply:
                    ev.message.reply(reply, False)
        except requests.exceptions.HTTPError as e:
            if "404 Client Error: Not Found for url:" in e and "/history" in e:
                return  # Return and do nothing.
            else:
                traceback.print_exc()
                raise e  # Raise an error if it's not the 'expected' nonexistent link error.

        # if result.message:
        #     message_with_reply = u":{} {}".format(message_id, result.message)
        #     if len(message_with_reply) <= 500 or "\n" in result.message:
        #         ev.message.reply(result.message, False)
        if result.command_status is False:
            pass
    except Exception:
        try:
            # log the error
            log_exception(*sys.exc_info())

            ev.message.reply("I hit an error while trying to run that command; run `!!/errorlogs` for details.")
            return
        except Exception:
            print("An exception was thrown while handling an exception: ")
            traceback.print_exc()


# noinspection PyMissingTypeHints
def handle_commands(content_lower, message_parts, ev_room, ev_room_name, ev_user_id, ev_user_name, wrap2, content,
                    message_id):
    message_url = "//chat.{host}/transcript/message/{id}#{id}".format(host=wrap2.host, id=message_id)
    # second_part_lower = "" if len(message_parts) < 2 else message_parts[1].lower()

    match = re.match(r"[!/]*[\w-]+", content_lower)
    command = match.group(0) if match else ""
    # if re.compile("^:[0-9]{4,}$").search(message_parts[0]):
    #     msg_id = int(message_parts[0][1:])
    #     msg = wrap2.get_message(msg_id)
    #     msg_content = msg.content_source
    #     quiet_action = ("-" in second_part_lower)
    #     if str(msg.owner.id) != bot_user_id[wrap2.host] or msg_content is None:
    #         return Response(command_status=False, message=None)
    #     post_url = fetch_post_url_from_msg_content(msg_content)
    #     post_site_id = fetch_post_id_and_site_from_msg_content(msg_content)
    #     if post_site_id is not None:
    #         post_type = post_site_id[2]
    #     else:
    #         post_type = None
    #
    #     subcommand_parameters = {
    #         'msg_content': msg_content,
    #         'ev_room': ev_room,
    #         'ev_room_name': ev_room_name,
    #         'ev_user_id': ev_user_id,
    #         'ev_user_name': ev_user_name,
    #         'message_url': message_url,
    #         'msg': msg,
    #         'post_site_id': post_site_id,
    #         'post_type': post_type,
    #         'post_url': post_url,
    #         'quiet_action': quiet_action,
    #         'second_part_lower': second_part_lower,
    #         'wrap2': wrap2,
    #     }
    #     if second_part_lower not in subcmds:
    #         return Response(command_status=False, message=None)  # Unrecognized subcommand
    #
    #     return subcmds[second_part_lower](**subcommand_parameters)

    # Process additional commands
    command_parameters = {
        'content': content,
        'content_lower': content_lower,
        'ev_room': ev_room,
        'ev_room_name': ev_room_name,
        'ev_user_id': ev_user_id,
        'ev_user_name': ev_user_name,
        'message_parts': message_parts,
        'message_url': message_url,
        'wrap2': wrap2,
    }

    if ev_user_id == GlobalValues.bot_user_id[wrap2.host]:
        return

    if command not in cmds:
        return Response(command_status=False, message=None)  # Unrecognized command, can be edited later.

    print(message_parts)
    return cmds[command](**command_parameters)
