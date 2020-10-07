#!/usr/bin/env python3

from subprocess import call
import base64

call(["gcc", "ahoc.c", "-o", "ahoc.o"])
call(["objcopy", "--only-section=.text", "-O", "binary", "ahoc.o", "text.o"])
with open("text.o", "rb") as fil:
    with open("text.py", "w") as ut:
        ut.write(f"base64.standard_b64decode({base64.standard_b64encode(fil.read())})")
