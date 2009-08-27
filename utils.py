# utils.py: Useful utilities for Pys60 programs
#
# Copyright (C) Lado Kumsiashvili, 2009
#
# Project URL: http://lado.dyndns.org/wiki/geoinput
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
import appuifw

def u(x) : return x.decode('utf-8')

def info(msg):
    appuifw.note(msg,"info",1)
###
def error(msg):
    appuifw.note(msg,"error",1)

###
def conf(msg):
    appuifw.note(msg,"conf",1)

def merge(list1, list2):
    for line in list2:
        if line not in list1:
            list1.append(line)
    return list1
