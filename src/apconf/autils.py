#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: bcabezas@apsl.net

import subprocess
from popen2 import Popen3
import logging 

log=logging.getLogger(__name__)

def call(cmd, raise_error=True):
    p = Popen3(cmd=cmd,capturestderr=True)
    res = p.wait()
    if res > 0 and raise_error:
        raise OSError(p.childerr.readline())
    return(res,p.fromchild,p.childerr)


def run(cmd, raise_error=True):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    out, err = p.communicate()
    res = p.returncode
    if res > 0 and raise_error:
        log.error(out)
        log.error(err)
        raise OSError(err)
        
    return (res, out, err)
