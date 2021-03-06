import os
import configparser

from common.constants import YETI_FEEDS_ROOT


class Dictionary(dict):

    def __getattr__(self, key):
        return self.get(key, None)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config:

    def __init__(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(os.path.join(YETI_FEEDS_ROOT, 'yeti_feeds.conf'))

        for section in config.sections():
            setattr(self, section, Dictionary())
            for name in config.options(section):
                try:
                    value = config.getint(section, name)
                except ValueError:
                    try:
                        value = config.getboolean(section, name)
                    except ValueError:
                        value = config.get(section, name)

                getattr(self, section)[name] = value

    def __getitem__(self, key):
        return getattr(self, key)

    def set_default_value(self, section, key, value):
        if not hasattr(self, section):
            setattr(self, section, Dictionary())

        if key not in self[section]:
            self[section][key] = value

    def get(self, section, key, default=None):
        if not hasattr(self, section) or key not in self[section]:
            return default

        return self[section][key]


yeti_feeds_config = Config()


yeti_feeds_config.set_default_value(
    'async', 'enabled', os.environ.get('YETI_ASYNC_ENABLED') or False)
yeti_feeds_config.set_default_value(
    'async', 'redis_server', os.environ.get('YETI_FEEDS_REDIS_SERVER') or '127.0.0.1')
yeti_feeds_config.set_default_value(
    'async', 'redis_port', os.environ.get('YETI_FEEDS_REDIS_PORT') or 6379)
