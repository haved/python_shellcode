import ctypes
import mmap
import array

libc = ctypes.cdll.LoadLibrary(None)
mmap_function = libc.mmap
mmap_function.restype = ctypes.c_void_p
mmap_function.argtypes = (ctypes.c_void_p, ctypes.c_size_t,
                          ctypes.c_int, ctypes.c_int,
                          ctypes.c_int, ctypes.c_size_t)
CODE_SIZE = 1000
DATA_SIZE = 100000
code_address = mmap_function(None, CODE_SIZE,
                             mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC,
                             mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS,
                             -1, 0)
if code_address == -1:
    raise OSError('mmap failed to allocate memory')

code=b'AWE1\xc0AVAUATUSH\x89T$\xf0\x85\xff\x0f\x8e8\x01\x00\x00\x8dG\x01Lc\xefA\x89\xf8I\x89\xf2\x0f\xaf\xc7I\x89\xd4J\x8d\x1c\xad\x00\x00\x00\x00E1\xdbH\x98H\xc1\xe0\x02H\x89D$\xe8I\x89\xc7M\x89\xe6L\x89\xd71\xed\x0f\x1f\x00\x89\xe91\xd2\xb8\x00\xe1\xf5\x05\x0f\x1f\x80\x00\x00\x00\x00\x8b4\x179\xf0\x0fO\xc6\x83\xc1\x01A\x89\x04\x16H\x01\xdaA9\xc8\x7f\xe9D\x8dM\x01H\x01\xdfM\x01\xfeE9\xc8t\x05D\x89\xcd\xeb\xc5I\x83\xc3\x01I\x83\xc2\x04I\x83\xc4\x04M9\xddu\xa9D\x89\xc8\xc7D$\xf8\x00\x00\x00\x00E1\xedE1\xc0\xf7\xd8\x89D$\xfc\x8bD$\xf8L\x8b|$\xf0E1\xf6D\x8dP\x01\x0f\x1fD\x00\x00A\xbc\x01\x00\x00\x00L\x89\xfeE\x89\xf3E)\xf4f\x0f\x1f\x84\x00\x00\x00\x00\x00C\x8d<\x1cL\x89\xea\xb9\x00\xe1\xf5\x05\x0f\x1f@\x00\x8b\x04\x969\xc1\x0fO\xc8A\x8d\x04\x12\x0f\xaf\xc1\x0f\xaf\xc7A9\xc0D\x0fL\xc0H\x83\xc2\x01A9\xd1\x7f\xdeA\x8dC\x01H\x01\xdeD9\xdd~\nA\x89\xc3\xeb\xbd\x0f\x1fD\x00\x00A\x8dF\x01L\x03|$\xe8D9\xf5t\x05A\x89\xc6\xeb\x8d\x83l$\xf8\x01I\x83\xc5\x01\x8bD$\xf89D$\xfc\x0f\x85a\xff\xff\xff[D\x89\xc0]A\\A]A^A_\xc3'
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

cuboid_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
cuboid_c = ctypes.cast(code_address, cuboid_type)

data_address = ctypes.cast(ctypes.create_string_buffer(DATA_SIZE),ctypes.POINTER(ctypes.c_void_p))

def largest_cuboid(tiles):
    n = len(tiles)
    print(n)
    heights = array.array('i')

    for row in tiles:
        for tile in row:
            heights.append(tile)

    array_address, _ = heights.buffer_info()
    return cuboid_c(n, array_address, data_address)

highscore = False
