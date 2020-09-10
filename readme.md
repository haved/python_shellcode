
# My attempt to make a queue in C and inject it into python
The c code is compiled into a byte object that python then places into an
exectuable and writeable mmapped block.

The c code is not linked, so can not use any external functions.
It can however use the Python.h header for macros and struct field offsets.

It defines a few functions, compiles it and copies the `.text` section
to a python bytes object. I have to use objdump to manually
see the offsets each function exists at.

Note: ctypes is only used for initial calls to C, which will then
change the function pointers associated with python functions.

This is all to try and get a good time on the INGInious scoreboard in TDT4120.

The version of python is different, so I compile my own from the cpython repository to test.

Python version on server:
```
import sys

ver = sys.version_info
assert ver.major == 3
assert ver.minor == 6
assert ver.micro == 8
```

ubuntu:18.04 docker image has `python3` package at `3.6.9`, which hopefully lets me test on a "different machine".
