# -*- coding: utf-8 -*-
from os import environ, path


class _Config(object):
    @property
    def TOKEN(self):
        env_token = environ.get('TELEGRAM_TOKEN')
        if env_token is not None:
            return env_token
        try:
            with open('.telegram.token') as f:
                return ''.join(f.readlines()).strip()
        except:
            raise RuntimeError(
                'Telegram token not set. Please make sure that you followed the instructions on README and that you '
                'have created the token file in `{}` and that is readable from the current user'.format(
                    path.join(path.abspath('.'), '.telegram.token')
                ),
            )

    WAITING_TIMEOUT = 60.0
    DELETE_JOIN = True


Config = _Config()
