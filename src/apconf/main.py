#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: bcabezas@apsl.net

__VERSION__ = '0.0.26'

from apconf.options import Options

from optparse import OptionParser
from pkg_resources import Requirement, resource_filename
import logging
import os
import sys

DEFAULT_CONFIG_FILE = "/etc/apconf.ini"
NAME = 'apconf'

log = logging.getLogger(NAME)


def main():
    """ Opciones de configuracion para apps django """

    parser = OptionParser(usage="usage: %prog [options] [VALUE]")
    #parser.add_option("-n", "--no-rotate",
                  #action="store_true", dest="no_rotate", default=False,
                  #help="rotate ftp files on upload cmd")
    parser.add_option("--version", "-v", action="store_true")
    parser.add_option("--list", "-l", action="store_true")
    parser.add_option("--get", "-g", action="store", dest="get_option")
    parser.add_option("--set", "-s", action="store", dest="set_option",
                help="set SET_OPTION parameter to VALUE")

    options, args = parser.parse_args()

    if options.version:
        print("%s v. %s") % (NAME, __VERSION__)
        return 0

    if os.path.isfile(DEFAULT_CONFIG_FILE):
        cfgfile = DEFAULT_CONFIG_FILE
    else:
        try:
            cfgfile = resource_filename(Requirement.parse("apconf"),
                   "apconf/conf/apconf-sample.ini")
            #log.warn("Usando sample config file: %s" % cfgfile)
        except:
            log.error("No se ha encontrado el fichero de configuración")
            parser.print_help()
            return 1

    opts = Options()

    if options.list:
        from clint.textui import puts, colored
        pformat = "%30s: %s"
        puts('')
        for section in opts.sections:
            puts(pformat % (colored.green("[%s]" % section), ''))
            #puts(pformat % (colored.white('Option'), colored.cyan('Value')))
            for key, value in opts.items(section):
                puts(pformat % (colored.blue(key), colored.white(value)))

            puts('')
    elif options.get_option:
        try:
            print(opts.get(options.get_option))
        except KeyError:
            parser.print_help()
            return 1
    elif options.set_option:
        try:
            opts.set(options.set_option, args[0])
            opts.write()
        except IndexError:
            parser.print_help()
            return 1
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
