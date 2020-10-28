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

#import base64
code=b'AVD\x8dv\xfeA\x89\xf9H\x89\xd7AUI\x89\xcdATA\x89\xf4USE\x85\xf6xlE\x8dA\x01\x8dF\xffE\x89\xcbE\x89\xf2D\x0f\xaf\xc0A\xf7\xd3A\x8di\xffH\x8dZ\x04\x0f\x1f\x80\x00\x00\x00\x00E\x85\xc9~7Ic\xd0C\x8d\x0c\x03H\x8dt\x15\x00Hc\xc9H\x8d\x04\x97H\x8d4\xb3H)\xd1\x90\x8bP\x049\x10\x0fN\x109P\x08\x0fNP\x08\x01T\x88\x04H\x83\xc0\x04H9\xc6u\xe4A\x83\xea\x01E\x01\xd8A\x83\xfa\xffu\xb7E\x85\xc9\x0f\x8e\x99\x00\x00\x00Mc\xc11\xd2\xbe\xff\xff\xff\x7f1\xc0f\x90\x8bL\x97\x049\xf1}\x04\x89\xce\x89\xd0H\x83\xc2\x01I9\xd0u\xebA\x89E\x00A\x83\xfc\x01~aA\x83\xc1\x01I\x8dM\x04O\x8d\\\xb5\x08D\x89\xca\xeb*\x0f\x1f\x80\x00\x00\x00\x00A\x89\xf0\x8d4\x02\x83\xe8\x01Hc\xf6D9\x04\xb7|\x03D\x89\xd0\x89\x01H\x83\xc1\x04D\x01\xcaI9\xcbt%D\x8dP\x01A\x8d4\x12Hc\xf6D\x8b\x04\xb7\x8dt\x10\x02Hc\xf6\x8b4\xb7D9\xc6|\xbfA\x89\xc2\xeb\xbdf\x90[1\xc0]A\\A]A^\xc31\xc0\xeb\x86'
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

seamcarve_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
seamcarve_c = ctypes.cast(code_address, seamcarve_type)

def find_path(weights):
    h = len(weights)
    w = len(weights[0])

    values = array.array('i', [w for row in weights for w in [0x7FFFFFFF]+row])
    values.append(0x7FFFFFFF)
    output = array.array('i', [0 for _ in range(h)])

    values_address, _ = values.buffer_info()
    output_address, _ = output.buffer_info()

    seamcarve_c(w, h, values_address, output_address)

    return list(zip(output, range(h)))

highscore = True

print(find_path([[1, 10, 3, 3], [1, 10, 3, 3], [10, 10, 3, 3]]))
