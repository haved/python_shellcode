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
DATA_SIZE = 100000
code_address = mmap_function(None, CODE_SIZE,
                             mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC,
                             mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS,
                             -1, 0)
if code_address == -1:
    raise OSError('mmap failed to allocate memory')

import base64
code=base64.standard_b64decode(b'8w8e+jHtSYnRXkiJ4kiD5PBQVEyNBZYEAABIjQ0fBAAASI09DQQAAP8Vki8AAPSQSI090S8AAEiNBcovAABIOfh0FUiLBW4vAABIhcB0Cf/gDx+AAAAAAMMPH4AAAAAASI09oS8AAEiNNZovAABIKf5IifBIwe4/SMH4A0gBxkjR/nQUSIsFRS8AAEiFwHQI/+BmDx9EAADDDx+AAAAAAPMPHvqAPV0vAAAAdTNVSIM9Ii8AAABIieV0DUiLPT4vAAD/FRAvAADoY////8YFNC8AAAFdw2YuDx+EAAAAAADDZmYuDx+EAAAAAAAPH0AA8w8e+uln////VUiJ5UiD7CBIiX3oSItF6EiLgOAAAABIhcB1YUiLRehIiwBIhcB0VUiLRehIiwBIicfoyf///0iJRfhIg334AHQpSItF6A+2gNgAAAAPvtBIi0X4idZIicfoLAAAAEiLVehIiYLgAAAA6xJIi0XoSIsQSItF6EiJkOAAAABIi0XoSIuA4AAAAMnDVUiJ5VNIg+woSIl92InwiEXUD75V1EiLRdhIY9JIi0TQCEiFwHVUSItF2EiLAEiFwHQ0SItF2EiJx+g3////SIlF6A++VdQPvl3USItF6InWSInH6Kf///9Ii1XYSGPLSIlEygjrFA++VdRIi0XYSGPSSItN2EiJTNAID75V1EiLRdhIY9JIi0TQCEiLXfjJw1VIieVIg+wQSIl9+EiLRfiLgOgAAACFwHlSSItF+IuA6AAAAI2QoIYBAEiLRfiJkOgAAABIi0X4SIsASIXAdCxIi0X4SInH6Jn+//9IicforP///4nCSItF+IuA6AAAAAHCSItF+ImQ6AAAAEiLRfiLgOgAAADJw1VIieVIg+xgSIl9uIl1tEiJVaiJTbBMiUWgx0XIAAAAAEiLRaBIiUXoi0XIjVABiVXISGPQSInQSMHgBEgp0EjB4ARIicJIi0XoSAHQSIlF8MdFzAAAAADp3AAAAEiLRfBIiUXY6ZsAAAAPtkXHg+hBiEXHD75Vx0iLRdhIY9JIi0TQCEiFwHVji0XIjVABiVXISGPQSInQSMHgBEgp0EjB4ARIicJIi0XoSAHQSIlF+EiLRfhIi1XYSIkQSItF+A+2VceIkNgAAABIi0X4x4DoAAAAYHn+/w++VcdIi0XYSGPSSItN+EiJTNAID75Vx0iLRdhIY9JIi0TQCEiJRdhIg0WoAUiLRagPtgCIRceAfccAD4VR////SItF2IuA6AAAAI1QAUiLRdiJkOgAAABIg0WoAYNFzAGLRcw7RbAPjBj////HRdAAAAAASItF8EiJReDHRdQAAAAA6z+LRdRIY9BIi0W4SAHQD7YAg+hBiEXGD75VxkiLReCJ1kiJx+hy/f//SIlF4EiLReBIicfo8/3//wFF0INF1AGLRdQ7RbR8uYtF0MnDVUiJ5bgAAAAAXcPzDx76QVdMjT27KQAAQVZJidZBVUmJ9UFUQYn8VUiNLawpAABTTCn9SIPsCOhv+///SMH9A3QfMdsPH4AAAAAATInyTInuRInnQf8U30iDwwFIOd116kiDxAhbXUFcQV1BXkFfw2ZmLg8fhAAAAAAA8w8e+sM=')
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

string_match_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p)
string_match_c = ctypes.cast(code_address+0x12ac-0x1020, string_match_type)

data = ctypes.create_string_buffer(DATA_SIZE)
data_address = ctypes.cast(data,ctypes.POINTER(ctypes.c_void_p))
ctypes.memset(data_address, DATA_SIZE, 0)

def string_match(dna, segments):
    dna_buf = dna.encode('utf-8')
    seg_buf = ('\0'.join(segments)+'\0').encode('utf-8')

    dna_len = len(dna_buf)
    seg_count = len(segments)
    return string_match_c(dna_buf, dna_len, seg_buf, seg_count, data_address)

highscore = False

dna = "ACTTACTGG"
segments = ["A", "ACT", "GG"]
print(string_match(dna, segments))
