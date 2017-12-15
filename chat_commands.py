# coding=utf-8

from helpers import Response, is_privileged
import random
from pytio import TioRequest
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


class TioCommands:

    @staticmethod
    def command_run(message_parts, ev_room, ev_user_name, wrap2, *args, **kwargs):
        if len(message_parts) <= 2:
            return Response(command_status=True, message=u"We need two things given with this command: the programming"
                                                         u" language of the code, *and* the code, in that order.")

        language = message_parts[1]

        if language not in GlobalValues.prog_languages:
            return Response(command_status=True, message=u"The specified programming language is not available in Tio.")

        code = " ".join(message_parts[2:])
        print("Language: {lang} | Code: {code}".format(lang=language, code=code))

        data = GlobalValues.tio.send(TioRequest(language, code))
        output_parts = []
        if data.error:
            spliterror = data.error.split('\n')
            for item in spliterror:
                output_parts.append("    {}\n".format(item))

        else:
            splitresult = data.result.split('\n')
            for item in splitresult:
                output_parts.append("    {}\n".format(item))

        wrap2.get_room(ev_room).send_message('    @{}\n{}'.format(ev_user_name, "".join(output_parts)))

        return

    @staticmethod
    def run_lang(message_parts, ev_room, ev_user_name, wrap2, *args, **kwargs):
        language = message_parts[0].replace(GlobalValues.chatprefix, '')
        code = ' '.join(message_parts[1:])
        parts = [GlobalValues.chatprefix + "run", language, code]
        TioCommands.command_run(message_parts=parts, ev_room=ev_room, ev_user_name=ev_user_name, wrap2=wrap2)
        pass


command_dict = {
    GlobalValues.chatprefix + "alive": AdminCommands.command_alive,
    GlobalValues.chatprefix + "ping": AdminCommands.command_alive,
    GlobalValues.chatprefix + "privileged": AdminCommands.command_privileged,
    GlobalValues.chatprefix + "amiprivileged": AdminCommands.command_privileged,
    GlobalValues.chatprefix + "run": TioCommands.command_run,
}

for lang in GlobalValues.prog_languages:
    command_dict[GlobalValues.chatprefix + lang] = TioCommands.run_lang
