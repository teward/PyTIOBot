# coding=utf-8

from helpers import Response, is_privileged
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

    # noinspection PyIncorrectDocstring,PyUnusedLocal,PyMissingTypeHints
    @staticmethod
    def command_privileged(ev_room, ev_user_id, wrap2, *args, **kwargs):
        """
        Tells user whether or not they have privileges
        :param wrap2:
        :param ev_user_id:
        :param ev_room:
        :param kwargs: No additional arguments expected
        :return: A string
        """
        if is_privileged(wrap2.host, ev_user_id, wrap2):
            return Response(command_status=True, message=u"\u2713 You are a privileged user.")
        else:
            return Response(command_status=True,
                            message=u"\u2573 " + GlobalValues.not_privileged_warning)


command_dict = {
    GlobalValues.chatprefix + "alive": AdminCommands.command_alive,
    GlobalValues.chatprefix + "ping": AdminCommands.command_alive,
    GlobalValues.chatprefix + "privileged": AdminCommands.command_privileged,
    GlobalValues.chatprefix + "amiprivileged": AdminCommands.command_privileged,
}
