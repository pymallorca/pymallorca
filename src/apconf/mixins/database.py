# -*- coding: utf-8 -*-

from apconf import Options

opts = Options()


def get(value, default):
    return opts.get(value, default, section='Database')


class DatabasesMixin(object):

    def DATABASES(self):
        engine = get('DATABASE_ENGINE', 'sqlite3')
        if 'django.db.backends' in engine:
            ENGINE = engine
        else:
            ENGINE = 'django.db.backends.' + engine

        return {
            'default': {
                'ENGINE': ENGINE,
                'NAME': get('DATABASE_NAME', 'db.sqlite'),
                'USER': get('DATABASE_USER', None),
                'PASSWORD': get('DATABASE_PASSWORD', ''),
                'HOST': get('DATABASE_HOST', ''),
                'PORT': get('DATABASE_PORT', ''),
                'OPTIONS': {},
            }
        }
