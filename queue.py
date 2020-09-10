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

code=b'UH\x89\xe5H\x89}\xf8H\x89u\xf0H\x8bE\xf8H\x8b@\x10H\x8bU\xf0H\x89P\x08\xb8\x00\x00\x00\x00]\xc3ff.\x0f\x1f\x84\x00\x00\x00\x00\x00f\x90UH\x89\xe5\x89}\xfcH\x89u\xf0H\x89U\xe8H\x8bE\xe8H\x83\xe8\x18H\xc7\x00\x00\x00\x00\x00H\x8bE\xe8H\x83\xe8\x10H\xc7\x00\x00\x00\x00\x00H\x8bE\xe8H\x8dP\xf8\x8bE\xfcH\x98H\x89\x02H\x8bE\xf0H\x8d\x90\x80\x00\x00\x00H\x8bE\xe8H\x89\x02\xb8\x00\x00\x00\x00]\xc3f.\x0f\x1f\x84\x00\x00\x00\x00\x00UH\x89\xe5H\x89}\xe8H\x89u\xe0H\x8bE\xe8H\x8b\x80\x80\x00\x00\x00H\x89E\xf8H\x8bE\xe0H\x8b\x00H\x8dP\x01H\x8bE\xe0H\x89\x10H\x8bE\xf8H\x8dP\xf0H\x8b\x02H\x8dH\x01H\x89\nH\x8bU\xf8H\x83\xea\x08H\x8b\n\xba\x00\x00\x00\x00H\xf7\xf1H\x89\xd0H\x8d\x14\xc5\x00\x00\x00\x00H\x8bE\xf8H\x01\xc2H\x8bE\xe0H\x89\x02H\x8bE\xe0H\x8b\x00H\x8dP\x01H\x8bE\xe0H\x89\x10H\x8bE\xe0]\xc3ff.\x0f\x1f\x84\x00\x00\x00\x00\x00f\x90UH\x89\xe5H\x89}\xe8H\x89u\xe0H\x8bE\xe8H\x8b\x80\x80\x00\x00\x00H\x89E\xf8H\x8bE\xf8H\x8dP\xe8H\x8b\x02H\x8dH\x01H\x89\nH\x8bU\xf8H\x83\xea\x08H\x8b\n\xba\x00\x00\x00\x00H\xf7\xf1H\x89\xd0H\x8d\x14\xc5\x00\x00\x00\x00H\x8bE\xf8H\x01\xd0H\x8b\x00]\xc3'
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

setCallAddress_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_void_p)
setCallAddress = ctypes.cast(code_address+0x00, setCallAddress_type)

setMaxSize_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.py_object, ctypes.c_void_p)
setMaxSize = ctypes.cast(code_address+0x30, setMaxSize_type)

import math
from math import gamma, floor

setCallAddress(gamma, code_address+0x90)
setCallAddress(floor, code_address+0x120)

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
