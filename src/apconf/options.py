#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# bcabezas@apsl.net

try:
    from configparser import ConfigParser, NoSectionError
except ImportError:
    pass
#from collections import namedtuple
import os
from os.path import join, pardir, abspath

DEFAULT_CONF_NAME = "app.ini"
DEFAULT_SECTION = "Base"


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


class Option(object):
    """Option Object"""

    def __init__(self, value=None, section=None, default_value=None):
        self.value = value
        self.section = section
        self.default_value = default_value

    def __repr__(self):
        return u'Option(value=%r, section=%r, default=%r)' % (self.value,
                self.section, self.default_value)

    def get_value_or_default(self):
        if self.value is not None:
            return self.value
        return self.default_value


@singleton
class Options(object):
    """Option Parser. By now based on ini files"""

    def __init__(self):
        """Parse initial options"""
        self.config = ConfigParser()
        self.config_file = None
        self._read_config()
        self.defaults = {}
        self.options = {}
        self._parse_options()

    def _conf_paths(self):
        paths = []
        current = abspath(".")
        while current != "/":
           paths.append(join(current, DEFAULT_CONF_NAME))
           current = abspath(join(current, pardir))
        return list(reversed(paths))
    
    def _read_config(self):
        try:
            self.config_file = self.config.read(self._conf_paths())[0]
        except IndexError:
            self.config_file = abspath(join('.', DEFAULT_CONF_NAME))

    def _cast_value(self, value):
        """Soportados: int, bool, str"""
        try:
            value = int(value)
        except ValueError:
            if value.lower().strip() in ["true", "t", "1", "yes"]:
                value = True
            elif value.lower().strip() in ["false", "f", "no", "0"]:
                value = False
        return value

    def _parse_options(self):
        """ Parsea fichero .ini y pone las opciones en self.options """
        for section in self.config.sections():
            for key, value in self.config.items(section=section):
                value = self._cast_value(value)
                self.options[key.upper()] = Option(value, section)

    def __iter__(self):
        """Return an iterator of options"""
        return (o for o in self.options.iteritems())

    @property
    def sections(self):
        """Get defined sections"""
        return set(o.section for k, o in self.options.iteritems())

    def items(self, section=None):
        """Iterate items of a section in format (name, value)"""
        if section:
            return ((k, o.value) for k, o in self.options.iteritems() if o.section == section)
        else:
            return ((k, o.value) for k, o in self.options.iteritems())

    def keys(self, section=None):
        """Returns all configured option names (keys)"""
        return [k for k, v in self.items(section)]

    def write(self):
        """Guarda todas las opciones definidas"""
        for name, option in self.options.iteritems():
            try:
                value = unicode(option.value)
            except UnicodeDecodeError:
                value = unicode(option.value, 'utf-8')

            try:
                self.config.set(section=option.section, option=name.upper(),
                        value=value)
            except NoSectionError:
                self.config.add_section(option.section)
                self.config.set(section=option.section, option=name,
                        value=value)
        self._write_file()

    def _write_file(self):
        import codecs
        with codecs.open(self.config_file, 'w', "utf-8") as config_file:
            self.config.write(config_file)

    def set(self, name, value, section=DEFAULT_SECTION):
        if type(value) == str:
            value = value.decode('utf-8')
        if name in self.options:
            self.options[name].value = value
        else:
            self.options[name] = Option(value, section)

    def get(self, name, default=None, section=DEFAULT_SECTION):
        """Returns value, and also saves the requested default
        If value exists in environ, return environ value"""

        try:
            self.options[name].default_value = default
            if not self.options[name].section:
                self.options[name].section = section
        except KeyError:
            self.options[name] = Option(value=None, section=section,
                   default_value=default)

        try:
            value = self._cast_value(os.environ[name])
            return value
        except KeyError:
            if self.options[name].value is not None:
                return self.options[name].value
            else:
                return default
