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

code=b'UH\x89\xe5H\x89}\xf8H\x8bE\xf8H\x8b\x00H\x8dP\x01H\x8bE\xf8H\x89\x10\x90]\xc3\x0f\x1f\x00UH\x89\xe5H\x89}\xe8H\x89u\xe0H\x8bE\xe8H\x8b@\x08H\x8b@8\x89E\xf4\x8bE\xf4Hc\xd0H\x8bE\xe8H\x01\xd0H\x89E\xf8H\x8bU\xe0H\x8bE\xf8H\x89\x10\x8bE\xf4]\xc3\x0f\x1f@\x00UH\x89\xe5H\x83\xec@H\x89}\xd8H\x89u\xd0H\x89U\xc8H\x89M\xc0H\x8bE\xd8H\x8b@\x08H\x8b@8\x89E\xec\x8bE\xecHc\xd0H\x8bE\xd8H\x01\xd0H\x8b\x00H\x89E\xf0H\x8bE\xf0H\x05\xa0\x03\x00\x00H\x89E\xf8H\x8bE\xf8H\xc7\x00\x00\x00\x00\x00H\x8bE\xf8H\x83\xc0\x08H\xc7\x00\x00\x00\x00\x00H\x8bE\xd8H\x89\xc7\xe81\xff\xff\xffH\x8bE\xd8\xc9\xc3ff.\x0f\x1f\x84\x00\x00\x00\x00\x00UH\x89\xe5H\x83\xec@H\x89}\xd8H\x89u\xd0H\x89U\xc8H\x89M\xc0H\x8bE\xd8H\x8b@\x08H\x8b@8\x89E\xe4\x8bE\xe4Hc\xd0H\x8bE\xd8H\x01\xd0H\x8b\x00H\x89E\xe8H\x8bE\xe8H\x05 \x03\x00\x00H\x89E\xf0H\x8bE\xd0H\x8b\x00H\x89E\xf8H\x8bE\xf8H\x89\xc7\xe8\xc0\xfe\xff\xffH\x8bE\xf0H\x8dP\x08H\x8b\x02H\x8dH\x01H\x89\nH\x8bU\xf0H\x83\xc2\x10H\x8b\n\xba\x00\x00\x00\x00H\xf7\xf1H\x89\xd0H\x83\xc0\x04H\x8d\x14\xc5\x00\x00\x00\x00H\x8bE\xf0H\x01\xc2H\x8bE\xf8H\x89\x02H\x8bE\xd8H\x89\xc7\xe8r\xfe\xff\xffH\x8bE\xd8\xc9\xc3ff.\x0f\x1f\x84\x00\x00\x00\x00\x00\x90UH\x89\xe5H\x89}\xd8H\x89u\xd0H\x89U\xc8H\x89M\xc0H\x8bE\xd8H\x8b@\x08H\x8b@8\x89E\xec\x8bE\xecHc\xd0H\x8bE\xd8H\x01\xd0H\x8b\x00H\x89E\xf0H\x8bE\xf0H\x05`\x02\x00\x00H\x89E\xf8H\x8bE\xf8H\x8b\x00H\x8dH\x01H\x8bU\xf8H\x89\nH\x8bU\xf8H\x83\xc2\x10H\x8b\n\xba\x00\x00\x00\x00H\xf7\xf1H\x89\xd0H\x83\xc0\x04H\x8d\x14\xc5\x00\x00\x00\x00H\x8bE\xf8H\x01\xd0H\x8b\x00]\xc3'
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

setCallAddress_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_void_p)
setCallAddress = ctypes.cast(code_address+0x20, setCallAddress_type)

print("code address:", hex(code_address))

def make_superqu(x):
    print("Hei")
def superenqu(x):
    print("uff")
def superdequ():
    print("fak")

setCallAddress(make_superqu, code_address+0x60)
setCallAddress(superenqu, code_address+0xe0)
setCallAddress(superdequ, code_address+0x1a0)

def getDataAt(offset):
    ptr = ctypes.cast(code_address+0x400+offset, ctypes.POINTER(ctypes.c_size_t))
    value = ptr.contents.value
    print("woah================================" + hex(value))


class Queue():
    def __init__(self, max_size):
        ctypes.memmove(code_address+0x400+16, max_size.to_bytes(8, 'little'), 8)
        make_superqu()
        self.enqueue = superenqu
        self.dequeue = superdequ
    def enqueue(self, x):
        pass
    def dequeue(self):
        pass

highscore = False

q = Queue(64)
q.enqueue(7)
q.enqueue(10)
print(q.dequeue())
q.enqueue(13)
print(q.dequeue())
print(q.dequeue())
