# coding=utf-8
from ChatExchange_Extension import Client
from datetime import datetime
# noinspection PyCompatibility
from configparser import ConfigParser
from pytio import Tio


class GlobalValues:

    tio = Tio()
    prog_languages = tio.query_languages()

    config = ConfigParser()
    config.read('config')
    username = config['DefaultLogin']['email']
    password = config['DefaultLogin']['password']

    bot_user_id = {'stackexchange.com':
                   config['chat.stackexchange.com']['bot_uid']
                   if config.has_option('chat.stackexchange.com', 'bot_uid') and
                   config.get('chat.stackexchange.com', 'bot_uid') is not None
                   else None,

                   'stackoverflow.com':
                   config['chat.stackoverflow.com']['bot_uid']
                   if config.has_option('chat.stackoverflow.com', 'bot_uid') and
                   config.get('chat.stackoverflow.com', 'bot_uid') is not None
                   else None,

                   'meta.stackexchange.com':
                   config['chat.meta.stackexchange.com']['bot_uid']
                   if config.has_option('chat.meta.stackexchange.com', 'bot_uid') and
                   config.get('chat.meta.stackexchange.com', 'bot_uid') is not None
                   else None
                   }

    se_chat = Client("stackexchange.com")
    mse_chat = Client("meta.stackexchange.com")
    so_chat = Client("stackoverflow.com")

    if config.has_section('chat.stackexchange.com') and \
            config.has_option('chat.stackexchange.com', 'enabled') and \
            config['chat.stackexchange.com']['enabled'].lower() == 'yes':

        se_autojoins = config['chat.stackexchange.com']['autojoins'].split(',')
    else:
        se_autojoins = None

    if config.has_section('chat.meta.stackexchange.com') and \
            config.has_option('chat.meta.stackexchange.com', 'enabled') and \
            config['chat.meta.stackexchange.com']['enabled'].lower() == 'yes':
        mse_autojoins = config['chat.stackexchange.com']['autojoins'].split(',')
    else:
        mse_autojoins = None

    if config.has_section('chat.stackoverflow.com') and \
            config.has_option('chat.stackoverflow.com', 'enabled') and \
            config['chat.stackoverflow.com']['enabled'].lower() == 'yes':
        so_autojoins = config['chat.stackexchange.com']['autojoins'].split(',')
    else:
        so_autojoins = None

    se_userid = config['chat.stackexchange.com']['bot_uid'] \
        if config.has_option('chat.stackexchange.com', 'bot_uid') and \
        config.get('chat.stackexchange.com', 'bot_uid') is not None else None
    se_botmaster_room_id = '68356'

    mse_userid = config['chat.meta.stackexchange.com']['bot_uid'] \
        if config.has_option('chat.meta.stackexchange.com', 'bot_uid') and \
        config.get('chat.meta.stackexchange.com', 'bot_uid') is not None else None

    so_userid = config['chat.stackoverflow.com']['bot_uid'] \
        if config.has_option('chat.stackoverflow.com', 'bot_uid') and \
        config.get('chat.stackoverflow.com', 'bot_uid') is not None else None

    privileged_users = {
        # This is actually chat.stackexchange.com, but is shortened for the 'host' CE data value
        'stackexchange.com': [
            10145,  # Thomas Ward, Bot Master
        ],

        # This is actually chat.meta.stackexchange.com, but is shortened for the 'host' CE data value
        'meta.stackexchange.com': [
            # No users at this time
        ],

        # This is actually chat.stackexchange.com, but is shortened for the 'host' CE data value
        'stackoverflow.com': [
            # No users at this time.
        ]
    }

    startup_utc = datetime.utcnow().strftime("%H:%M:%S")

    if config.has_section('ChatDefaults') and config.has_option('ChatDefaults', 'prefix'):
        chatprefix = config['ChatDefaults']['prefix'].lower()
    else:
        chatprefix = '!!/'

    bot_name = "PyTIOBot"

    not_privileged_warning = "You are not a privileged user. " \
                             "Go talk to my botmaster if you think you should be privileged."
