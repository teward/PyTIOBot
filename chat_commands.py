# coding=utf-8

from helpers import Response
import random
from globalvalues import GlobalValues


# # Functions go before the final dictionaries of command to function mappings
# def post_message_in_room(known_rooms, room_host, room_id_str, msg, length_check=True):
#     if room_id_str == GlobalVars.charcoal_room_id:
#         GlobalVars.charcoal_hq.send_message(msg, length_check)
#     elif room_id_str == GlobalVars.meta_tavern_room_id:
#         GlobalVars.tavern_on_the_meta.send_message(msg, length_check)
#     elif room_id_str == GlobalVars.socvr_room_id:
#         GlobalVars.socvr.send_message(msg, length_check)


class AdminCommands:
    # noinspection PyIncorrectDocstring,PyUnusedLocal
    @staticmethod
    def command_alive(ev_room, *args, **kwargs):
        """
        Returns a string indicating the process is still active
        :param ev_room:
        :param kwargs: No additional arguments expected
        :return: A string
        """
        return Response(command_status=True,
                        message=random.choice(['Yup', 'You doubt me?', 'Of course',
                                               '... did I miss something?', 'plz send teh coffee',
                                               'Watching this endless list of new questions *never* gets boring',
                                               'Kinda sorta']))


command_dict = {
    # "!!/run": command_run,
    GlobalValues.chatprefix + "alive": AdminCommands.command_alive,
    # "!!/ping": command_ping,
}
