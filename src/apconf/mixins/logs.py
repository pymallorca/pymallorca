# -*- coding: utf-8 -*-

from apconf import Options

opts = Options()


def get(value, default):
    return opts.get(value, default, section='Logs')


class LogsMixin(object):
    """Django Logging configuration"""

    @property
    def LOG_LEVEL(self):
        return get('LOG_LEVEL', 'DEBUG').upper()

    @property
    def DJANGO_LOG_LEVEL(self):
        return get('DJANGO_LOG_LEVEL', 'ERROR').upper()

    @property
    def LOG_FILE(self):
        return get('LOG_FILE', '')

    @property
    def SENTRY_ENABLED(self):
        enabled = get('SENTRY_ENABLED', False)
        try:
            import raven
        except ImportError:
            return False

        if enabled:
            self.add_sentry_to_installed_apps()
        return enabled


    @property
    def SENTRY_DSN(self):
        return get('SENTRY_DSN', '')

    @property
    def LOGGING(self):
        return {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': self.formatters,
            'filters': self.filters,
            'handlers': self.handlers,
            'loggers': self.loggers,
        }

    @property
    def handlers(self):
        handlers = {}

        handlers['default'] = {
                'level': self.LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'apsldefault'
                }

        if self.LOG_FILE:
            handlers['default']['class'] = 'logging.FileHandler'
            handlers['default']['filename'] = self.LOG_FILE

        handlers['mail_admins'] = {
                    'level': 'ERROR',
                    'filters': ['require_debug_false'],
                    'class': 'django.utils.log.AdminEmailHandler'
                }

        if self.SENTRY_ENABLED:
            handlers['sentry'] = {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            }

        return handlers

    @property
    def loggers(self):
        loggers = {}

        loggers[''] = {
                'handlers': ['default'],
                'level': self.LOG_LEVEL,
                'propagate': True,
            }

        loggers['rq.worker'] = {
                'handlers': ['default'],
                'level': self.LOG_LEVEL,
                'propagate': False,
            }

        loggers['django'] = {
                'handlers': ['default'],
                'level': self.DJANGO_LOG_LEVEL,
                'propagate': False,
            }

        if self.SENTRY_ENABLED:
            loggers['']['handlers'].append('sentry')
            loggers['django']['handlers'].append('sentry')
            loggers['raven'] = {
                    'handlers': ['default'],
                    'level': self.LOG_LEVEL,
                    'propagate': False,
                }
            loggers['sentry.errors'] = {
                    'handlers': ['default'],
                    'level': self.LOG_LEVEL,
                    'propagate': False,
                }

        return loggers

    @property
    def formatters(self):
        return {
            'apsldefault': {
                'format': "[%(asctime)s] %(levelname)s %(name)s-%(lineno)s %(message)s"
            }
        }

    @property
    def filters(self):
        return {
                'require_debug_false': {
                    '()': 'django.utils.log.RequireDebugFalse',
                }
            }

    def add_sentry_to_installed_apps(self):
        if not 'raven.contrib.django.raven_compat' in self.INSTALLED_APPS:
            self.INSTALLED_APPS += ('raven.contrib.django.raven_compat', )
