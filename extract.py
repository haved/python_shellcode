#!/usr/bin/env python3

from subprocess import call

call(["gcc", "-I/home/havard/Development/cpython/Include", "-I/home/havard/Development/cpython", "-c", "queuemodule.c", "-o", "queuemodule.o"])
call(["objcopy", "--only-section=.text", "-O", "binary", "queuemodule.o", "text.o"])
with open("text.o", "rb") as fil:
    with open("text.py", "w") as ut:
        ut.write(str(fil.read()))
