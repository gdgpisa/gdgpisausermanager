# -*- coding: utf-8 -*-
import os


class _Config(object):
    @property
    def TOKEN(self):
        try:
            with open('.telegram.token') as f:
                return ''.join(f.readlines()).strip()
        except:
            raise RuntimeError(
                'Telegram token not set. Please make sure that you followed the instructions on README and that you '
                'have created the token file in `{}` and that is readable from the current user'.format(
                    os.path.join(os.path.abspath('.'), '.telegram.token')
                ),
            )

    WAITING_TIMEOUT = 30.0


Config = _Config()
