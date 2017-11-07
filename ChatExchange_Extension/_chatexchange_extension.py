# coding=utf-8
from ChatExchange.chatexchange import client, rooms
import sys
from datetime import datetime
from termcolor import colored
# noinspection PyCompatibility
from configparser import ConfigParser


config = ConfigParser()
config.read('config')


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


class Room(rooms.Room):
    last_activity = datetime.utcnow()

    def send_message(self, text, length_check=True):
        if "no-chat" in sys.argv:
            log('info', "Blocked message to {0} due to no-chat setting: {1}".format(self.name, text))
            return

        if "charcoal-hq-only" not in sys.argv or int(self.id) == 11540:
            return rooms.Room.send_message(self, text, length_check)
        else:
            log('info', "Blocked message to {0} due to charcoal-hq-only setting: {1}".format(self.name, text))

    def watch_socket(self, event_callback):
        if "no-chat" in sys.argv:
            log('info', "Blocked socket connection to {0} due to no-chat setting".format(self.name))
            return

        def on_activity(activity):
            self.last_activity = datetime.utcnow()
            for event in self._events_from_activity(activity, self.id):
                event_callback(event, self._client)

        return self._client._br.watch_room_socket(self.id, on_activity)


class Client(client.Client):
    def get_room(self, room_id, **attrs_to_set):
        return self._get_and_set_deduplicated(
            Room, room_id, self._rooms, attrs_to_set)
