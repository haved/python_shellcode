import ctypes
import mmap
import array

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

import base64
code=base64.standard_b64decode(b'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')
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

powergrid_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
powergrid_c = ctypes.cast(code_address+0x410, powergrid_type)

MEM_SIZE = 50000000
data_address = ctypes.create_string_buffer(MEM_SIZE)

def power_grid(width, height, stations):
    if len(stations) <= 1:
        return 0
    values = array.array('i', [x for station in stations for x in station])

    values_address, _ = values.buffer_info()

    ctypes.memset(data_address, 0, width*height*4)

    return powergrid_c(width, height, len(stations), values_address, data_address)

highscore = True

tests = [
    ((2, 2, [(1, 1)]), 0),
    ((2, 2, [(0, 0), (1, 1)]), 2),
    ((2, 2, [(0, 0), (0, 1), (1, 0)]), 2),
    ((2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]), 3),
    ((3, 3, [(0, 2), (2, 0)]), 4),
    ((3, 3, [(0, 0), (1, 1), (2, 2)]), 4),
    ((3, 3, [(1, 1), (0, 1), (2, 1)]), 2),
    ((3, 3, [(1, 2)]), 0),
    ((3, 3, [(2, 0), (1, 1), (0, 1)]), 3),
    ((2, 3, [(1, 1)]), 0),
    ((2, 2, [(0, 1), (1, 0), (1, 1), (0, 0)]), 3),
    ((2, 2, [(0, 1), (1, 0), (1, 1), (0, 0)]), 3),
    ((3, 3, [(0, 1), (0, 2), (2, 1), (2, 2)]), 4),
    ((3, 3, [(0, 1), (0, 2), (1, 2), (2, 1)]), 4),
    ((2, 3, [(1, 0), (1, 1), (0, 2)]), 3),
    ((2, 3, [(1, 0)]), 0),
    ((3, 2, [(1, 0), (2, 1), (0, 0)]), 3),
    ((3, 3, [(0, 1), (1, 1), (2, 1), (0, 0)]), 3),
    ((3, 3, [(0, 2)]), 0),
]

for test_case, answer in tests:
    m, n, substations = test_case
    student = power_grid(m, n, substations)
    if student != answer:
        response = (
            "Koden feilet for følgende input: "
            + "(m={:}, n={:}, substations={:}). ".format(m, n, substations)
            + "Din output: {:}. Riktig output: {:}".format(student, answer)
        )
        print(response)
        break
