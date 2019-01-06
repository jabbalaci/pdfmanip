#!/usr/bin/env python3

"""
pynt's build file
https://github.com/rags/pynt

Usage:

$ pynt
"""

import os

from pynt import task


def call_external_command(cmd):
    print(f"┌ start: calling external command '{cmd}'")
    os.system(cmd)
    print(f"└ end: calling external command '{cmd}'")


###########
## Tasks ##
###########

@task()
def mypy():
    """
    run mypy
    """
    cmd = "mypy --config-file mypy.ini pdfmanip.py"
    call_external_command(cmd)
