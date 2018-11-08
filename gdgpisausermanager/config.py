# -*- coding: utf-8 -*-
import os


class _Config(object):
    @property
    def TOKEN(self):
        telegram_token_path = os.environ.get('TELEGRAM_TOKEN_PATH') or '.telegram.token'
        try:
            with open(telegram_token_path) as f:
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
