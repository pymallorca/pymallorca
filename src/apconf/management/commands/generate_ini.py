# -*- coding: utf-8 -*-
# @author: bcabezas@apsl.net

from django.core.management.base import NoArgsCommand

from apconf import Options


def module_to_dict(module, omittable=lambda k: k.startswith('_')):
    "Converts a module namespace to a Python dictionary. Used by get_settings_diff."
    return dict([(k, repr(v)) for k, v in module.__dict__.items() if not omittable(k)])


class Command(NoArgsCommand):
    help = """Displays differences between the current settings.py and Django's
    default settings. Settings that don't appear in the defaults are
    followed by "###"."""

    requires_model_validation = False

    def handle_noargs(self, **options):
        # Inspired by Postfix's "postconf -n".
        from django.conf import settings

        # Because settings are imported lazily, we need to explicitly load them.
        settings._setup()

        user_settings = module_to_dict(settings._wrapped)
        
        opts = Options()
        from clint.textui import puts, colored
        pformat = "%-25s = %s"
        puts('')
        for section in opts.sections:
            puts(colored.green("[%s]" % section))
            for key, apconf_value in opts.items(section):
                keycolor = colored.magenta(key)
                if key in user_settings:
                    #value = colored.green(user_settings[key])
                    keycolor = colored.blue(key)
                #else:
                    #value = colored.green(opts.options[key].get_value_or_default())

                default_value = opts.options[key].default_value
                #apconf_value = apconf_value if apconf_value else '-'

                value = apconf_value or default_value
                value = unicode(value).encode('utf8')

                try:
                    puts(pformat % (
                        keycolor,
                        value))
                except Exception as e:
                    raise e
            puts('')
