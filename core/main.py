from genericpath import isdir
import os
import time
from pathlib import Path
import configparser

import requests
from PySide6.QtCore import QObject, Slot, Signal


import threading
import functools


THREADS: list[threading.Thread] = []


def separate_thread(func):
    """Декоратор для выполнения функции в отдельном потоке"""
    @functools.wraps(func)
    def inner(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
    return inner


class Monitor(QObject):

    _username: str = ''
    _stats_url: str
    _feed_url: str

    _subscriptions: int = 0
    _subscribers: int = 0
    _likes: int = 0

    _display_name: str = ''
    _link: str = ''
    _avatar_link: str = ''

    _config_path: str = 'settings.ini'

    dataUpdated = Signal()
    userDataUpdated = Signal()

    def __init__(self):
        QObject.__init__(self)
        self._get_username()
        self._update_daemon()

    @Slot(result=str)
    def get_username(self) -> str:
        return self._username

    @Slot(result=str)
    def get_display_name(self) -> str:
        return self._display_name

    @Slot(result=str)
    def get_link(self) -> str:
        return self._link

    @Slot(result=int)
    def get_subscriptions(self) -> int:
        return self._subscriptions

    @Slot(result=int)
    def get_subscribers(self) -> int:
        return self._subscribers

    @Slot(result=int)
    def get_likes(self) -> int:
        return self._likes

    @Slot(result=str)
    def get_avatar_link(self) -> str:
        return self._avatar_link

    @Slot(str)
    @separate_thread
    def set_username(self, username: str):
        self._username = username
        self._set_urls()
        self.update_user_data()
        self.update_stats()
        self._save_username()

    def update_stats(self):
        data = requests.get(self._stats_url).json()
        self._subscriptions = data['subscriptions']
        self._subscribers = data['subscribers']
        self._likes = data['likes']
        self.dataUpdated.emit()
        print(data)

    def update_user_data(self):
        data = requests.get(self._feed_url).json()
        user_data = data['posts'][0]['user']

        self._display_name = user_data['displayName']
        self._link = user_data['shareLink']
        self._avatar_link = user_data['avatarURL']
        self.userDataUpdated.emit()

    def _get_username(self):
        config = config = self._get_config()
        self.set_username(config['DEFAULT']['username'])

    def _save_username(self):
        config = self._get_config()
        config['DEFAULT']['username'] = self._username

        with open(self._config_path, 'w') as configfile:
            config.write(configfile)

    def _get_config(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        if not os.path.isfile(self._config_path):
            self._config_path = '_internal/' + self._config_path
        config.read(self._config_path)
        return config

    def _set_urls(self):
        self._stats_url = f'https://shedevrum.ai/api/v1/users/{self._username}/social_stats?appPlatform=web'
        self._feed_url = f'https://shedevrum.ai/api/v1/users/{self._username}/feed?content=combined&amount=1&appPlatform=web'

    @separate_thread
    def _update_daemon(self):
        while True:
            time.sleep(10)
            self.update_stats()
