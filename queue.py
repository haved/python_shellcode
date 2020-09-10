import ctypes
import mmap

libc = ctypes.cdll.LoadLibrary(None)
mmap_function = libc.mmap
mmap_function.restype = ctypes.c_void_p
mmap_function.argtypes = (ctypes.c_void_p, ctypes.c_size_t,
                          ctypes.c_int, ctypes.c_int,
                          ctypes.c_int, ctypes.c_size_t)
CODE_SIZE = 10000000
code_address = mmap_function(None, CODE_SIZE,
                             mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC,
                             mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS,
                             -1, 0)
if code_address == -1:
    raise OSError('mmap failed to allocate memory')

code=b'H\x8bG\x10H\x89p\x081\xc0\xc3\x0f\x1fD\x00\x00Hc\xffH\xc7B\xe8\x00\x00\x00\x001\xc0H\xc7B\xf0\x00\x00\x00\x00H\x89z\xf8H\x89\x96\x80\x00\x00\x00\xc3ff.\x0f\x1f\x84\x00\x00\x00\x00\x00\x0f\x1f@\x00H\x8b\x8f\x80\x00\x00\x00H\x83\x06\x01H\x8bA\xf0H\x8dP\x01H\x89Q\xf01\xd2H\xf7q\xf8H\x89\xf0H\x894\xd1H\x83\x06\x01\xc3\x0f\x1f\x80\x00\x00\x00\x00H\x8b\x8f\x80\x00\x00\x00H\x8bA\xe8H\x8dP\x01H\x89Q\xe81\xd2H\xf7q\xf8H\x8b\x04\xd1\xc3'
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

setCallAddress_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_void_p)
setCallAddress = ctypes.cast(code_address+0x00, setCallAddress_type)

setMaxSize_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.py_object, ctypes.c_void_p)
setMaxSize = ctypes.cast(code_address+0x10, setMaxSize_type)

import math
from math import gamma, floor

setCallAddress(gamma, code_address+0x40)
setCallAddress(floor, code_address+0x70)

class Queue():
    def __init__(self, max_size):
        setMaxSize(max_size, math, code_address+0x200)
        self.enqueue = math.gamma
        self.dequeue = lambda: math.floor(0)
    def enqueue(self, x):
        pass
    def dequeue(self):
        pass

highscore = False

q = Queue(3)

liste = [1, 7, 3]
ops = [True, False, True, False, True, False]

ut = []

index = 0
for op in ops:
    if op:
        q.enqueue(liste[index])
        index += 1
    else:
        ut.append(q.dequeue())
print(liste, "== ? ==", ut)
