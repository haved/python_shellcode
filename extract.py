#!/usr/bin/env python3

from subprocess import call

FILE = "build/lib.linux-x86_64-3.8/queuemodule.cpython-38-x86_64-linux-gnu.so"

#call(["python", "setup.py", "build"])
#call(["objcopy", "--only-section=.text", "-O", "binary", FILE, "text.o"])
call(["gcc", "-I/usr/include/python3.8/", "-c", "queuemodule.c", "-o", "queuemodule.o"])
#call(["gcc", "queuemodule.o", "-o", "a.o"])
call(["objcopy", "--only-section=.text", "-O", "binary", "queuemodule.o", "text.o"])
with open("text.o", "rb") as fil:
    with open("text.py", "w") as ut:
        ut.write(str(fil.read()))
