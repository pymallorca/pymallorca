# -*- coding: utf-8 -*-

from apconf import Options

opts = Options()


def get(value, default):
    """opts.get wrapper para esta seccion.
    Usado para no llama cada vez  a la seccion.
    """
    return opts.get(value, default, section='Cache')


class CachesMixin(object):

    @property
    def REDIS_HOST(self):
        return get('REDIS_HOST', 'localhost')

    @property
    def REDIS_PORT(self):
        return get('REDIS_PORT', 6379)

    @property
    def CACHES(self):
        CACHE_TYPE = get('CACHE_TYPE', 'locmem')
        CACHE_REDIS_DB = get('CACHE_REDIS_DB', 2)
        CACHE_PREFIX = get('CACHE_PREFIX', self.APP_SLUG)
        CACHE_TIMEOUT = get('CACHE_TIMEOUT', 3600)
        CACHE_MAX_ENTRIES = get('CACHE_MAX_ENTRIES', 10000)

        if CACHE_TYPE == 'redis':
            CACHE = {
                'BACKEND': 'redis_cache.cache.RedisCache',
                'LOCATION': '%s:%s:%s' % (self.REDIS_HOST, self.REDIS_PORT, CACHE_REDIS_DB),
                'CACHE_PREFIX': CACHE_PREFIX,
                'OPTIONS': {
                    'TIMEOUT': CACHE_TIMEOUT,
                    'KEY_PREFIX': CACHE_PREFIX,
                    'MAX_ENTRIES': CACHE_MAX_ENTRIES,
                },
            }
        elif CACHE_TYPE == 'locmem':
            CACHE = {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'CACHE_PREFIX': CACHE_PREFIX,
                'LOCATION': 'unique-key-apsl'
            }
        else:
            CACHE = {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }

        return {'default': CACHE}
