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

code=b'UH\x89\xe5H\x89}\xf8H\x8bE\xf8H\x8b\x00H\x8dP\x01H\x8bE\xf8H\x89\x10\x90]\xc3UH\x89\xe5\x90]\xc3UH\x89\xe5H\x89}\xe8H\x89u\xe0H\x8bE\xe8H\x8b@\x08H\x8bU\xe0H\x89\x90\x80\x00\x00\x00\xe8\x00\x00\x00\x00XH\x89E\xf8H\x8bE\xf8]\xc3UH\x89\xe5H\x83\xec(H\x89}\xe8H\x89u\xe0H\x89U\xd8H\x8bE\xe0H\x8b@\x18H\x89E\xf8H\x8bE\xe8H\x89\xc7\xe8\x81\xff\xff\xffH\x8bE\xe8\xc9\xc3'

assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

setCallAddress_type = ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.py_object, ctypes.c_size_t)
setCallAddress = ctypes.cast(code_address+0x24, setCallAddress_type)

print("id(max):", id(max))
print("code address:", code_address)
data = setCallAddress(max, code_address+0x53) # address of make_superqu
print(data)
print(max(55))

highscore = False


