# coding=utf-8
from ChatExchange_Extension import Client
from datetime import datetime
# noinspection PyCompatibility
from configparser import ConfigParser, RawConfigParser


class GlobalValues:
    bot_user_id = {'stackexchange.com': '', 'stackoverflow.com': None, 'meta.stackexchange.com': None}

    config = ConfigParser()
    config.read('config')
    username = config['DefaultLogin']['email']
    password = config['DefaultLogin']['password']

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

    se_userid = None
    se_botmaster_room_id = '68356'

    mse_userid = None

    so_userid = None

    se_privileged_users = []
    so_privileged_users = []
    metase_privileged_users = []

    startup_utc = datetime.utcnow().strftime("%H:%M:%S")

    if config.has_section('ChatDefaults') and config.has_option('ChatDefaults', 'prefix'):
        chatprefix = config['ChatDefaults']['prefix'].lower()
    else:
        chatprefix = '!!/'

    bot_name = "PyTIOBot"

