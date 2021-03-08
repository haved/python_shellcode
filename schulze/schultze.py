import ctypes
import mmap
import array
import functools

libc = ctypes.cdll.LoadLibrary(None)
mmap_function = libc.mmap
mmap_function.restype = ctypes.c_void_p
mmap_function.argtypes = (ctypes.c_void_p, ctypes.c_size_t,
                          ctypes.c_int, ctypes.c_int,
                          ctypes.c_int, ctypes.c_size_t)
CODE_SIZE = 10000
code_address = mmap_function(None, CODE_SIZE,
                             mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC,
                             mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS,
                             -1, 0)
if code_address == -1:
    raise OSError('mmap failed to allocate memory')

code=b'\x85\xff\x0f\x8e\xfb\x00\x00\x00\x8dG\xffA\x89\xf9AWE1\xdbAVI\xf7\xd9L\x8dt\x86\x04AUL\x89\xf1I\x89\xf5I\xc1\xe1\x02ATUSHc\xdfL\x8d\x04\x9d\x00\x00\x00\x00\x0f\x1f\x84\x00\x00\x00\x00\x00I\x8d\x04\tH\x89\xf2f\x0f\x1f\x84\x00\x00\x00\x00\x00D\x8b\x12D9\x10\x7f\x06\xc7\x00\x00\x00\x00\x00H\x83\xc0\x04L\x01\xc2H9\xc8u\xe6A\x8dS\x01J\x8d\x0c\x00H\x83\xc6\x049\xd7t\x05A\x89\xd3\xeb\xc1E1\xd21\xedE1\xe4f\x0f\x1f\x84\x00\x00\x00\x00\x00L\x89\xeeL\x89\xf7H\x89\xe9E1\xc9L)\xd6\x90I\x8d\x142\x0f\x1f@\x00D\x8b:\x8b\x069\x04\x8a\x0fN\x04\x8aD9\xf8A\x0fL\xc7H\x83\xc2\x04\x89B\xfcH9\xd7u\xe1A\x8dA\x01H)\xd9L\x01\xc6L\x01\xc7E9\xcbt\x07A\x89\xc1\xeb\xc2f\x90A\x8dD$\x01H\x01\xddI\x83\xea\x04E9\xe3t\x05A\x89\xc4\xeb\x9a[1\xc0]A\\A]A^A_\xc31\xc0\xc3'
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

schulze_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_void_p)
schulze_c = ctypes.cast(code_address, schulze_type)

def schulze_method(A):
    n = len(A)

    values = array.array('i', [i for row in A for i in row])

    values_address, _ = values.buffer_info()

    schulze_c(n, values_address)

    result = [i for i in range(n)]
    def compare(i, j):
        if values[i*n+j] > values[j*n+i]:
            return 1
        if values[i*n+j] < values[j*n+i]:
            return -1
        if i < j:
            return 1
        elif i > j:
            return -1
        return 0
    result.sort(key=functools.cmp_to_key(compare),reverse=True)
    return result

highscore = True
