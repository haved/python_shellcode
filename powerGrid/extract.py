#!/usr/bin/env python3

from subprocess import call
import base64

call(["gcc", "-O2", "powergrid.c", "-o", "powergrid.o"])
call(["objcopy", "--only-section=.text", "-O", "binary", "powergrid.o", "text.o"])
with open("text.o", "rb") as fil:
    with open("text.py", "w") as ut:
        textStart = 0x1040
        myStart = 0x1150
        myEntry = 0x1560
        myEnd = 0x1970

        data = fil.read()[myStart-textStart:myEnd-textStart]
        print(f"Du starter ved: {myEntry-myStart:0x}")
        #ut.write(str(fil.read()))
        ut.write(f"base64.standard_b64decode({base64.standard_b64encode(data)})")
