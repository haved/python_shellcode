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

code=b'H\x8bG\x10H\x89p\x081\xc0\xc3\x0f\x1fD\x00\x00f\x0f\xef\xc01\xc0\x0f\x11B\xf0H\x89\x96\x80\x00\x00\x00\xc3ff.\x0f\x1f\x84\x00\x00\x00\x00\x00\x0f\x1f\x00H\x8b\x97\x80\x00\x00\x00H\x83\x06\x01H\x89\xf0H\x8bJ\xf8H\x8dq\x01H\x89r\xf8H\x89\x04\xcaH\x83\x00\x01\xc3ff.\x0f\x1f\x84\x00\x00\x00\x00\x00f\x90H\x8b\x87\x80\x00\x00\x00H\x8bP\xf0H\x8dJ\x01H\x89H\xf0H\x8b\x04\xd0\xc3'
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

setCallAddress_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_void_p)
setCallAddress = ctypes.cast(code_address+0x00, setCallAddress_type)

setMaxSize_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.py_object, ctypes.c_void_p)
setMaxSize = ctypes.cast(code_address+0x10, setMaxSize_type)

import readline
from readline import insert_text, get_completer

setCallAddress(insert_text, code_address+0x30)
setCallAddress(get_completer, code_address+0x60)

class Queue():
    def __init__(self, max_size):
        setMaxSize(max_size, readline, code_address+0x200)
        self.enqueue = insert_text
        self.dequeue = get_completer
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

