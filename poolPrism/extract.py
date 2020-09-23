#!/usr/bin/env python3

from subprocess import call

call(["gcc", "-O3", "-c", "pool.c", "-o", "pool.o"])
call(["objcopy", "--only-section=.text", "-O", "binary", "pool.o", "text.o"])
with open("text.o", "rb") as fil:
    with open("text.py", "w") as ut:
        ut.write(str(fil.read()))
