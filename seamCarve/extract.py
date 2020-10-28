#!/usr/bin/env python3

from subprocess import call
import base64

call(["gcc", "-O2", "-c", "seamcarve.c", "-o", "seamcarve.o"])
call(["objcopy", "--only-section=.text", "-O", "binary", "seamcarve.o", "text.o"])
with open("text.o", "rb") as fil:
    with open("text.py", "w") as ut:
        ut.write(str(fil.read()))
        #ut.write(f"base64.standard_b64decode({base64.standard_b64encode(fil.read())})")
