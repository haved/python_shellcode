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
DATA_SIZE = 50000000
code_address = mmap_function(None, CODE_SIZE,
                             mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC,
                             mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS,
                             -1, 0)
if code_address == -1:
    raise OSError('mmap failed to allocate memory')

import base64
code=base64.standard_b64decode(b'McDDZi4PH4QAAAAAAA8fAPMPHvox7UmJ0V5IieJIg+TwUFRMjQUWCAAASI0NnwcAAEiNPcj/////FYIvAAD0kEiNPcEvAABIjQW6LwAASDn4dBVIiwVeLwAASIXAdAn/4A8fgAAAAADDDx+AAAAAAEiNPZEvAABIjTWKLwAASCn+SInwSMHuP0jB+ANIAcZI0f50FEiLBTUvAABIhcB0CP/gZg8fRAAAww8fgAAAAADzDx76gD1NLwAAAHUzVUiDPRIvAAAASInldA1Iiz0uLwAA/xUALwAA6GP////GBSQvAAABXcNmLg8fhAAAAAAAw2ZmLg8fhAAAAAAADx9AAPMPHvrpZ////w8fgAAAAABBVFVTSA++3kiLRN8ISIXAdA5bXUFcw2YPH4QAAAAAAEiJ/UiLP0iF/3QlTIuF4AAAAEQPvuZNhcB0JUSJ5kyJx+i6////SIlE3QhbXUFcw0iJbN0ISInoW11BXMMPHwDoOwAAAEiJx0iFwHQbD7612AAAAOiH////SImF4AAAAEmJwOu2Dx8ATItFAEyJheAAAADrpmZmLg8fhAAAAAAAQVRTSIPsCEyLp+AAAABNheR0DUiDxAhMieBbQVzDZpBMiydIiftNheR06EmLvCTgAAAASIX/dBgPvrPYAAAA6Bz///9IiYPgAAAASYnE68NJizwkSIX/dC7oov///0iJx0iFwHQqQQ++tCTYAAAA6Oz+//9JiYQk4AAAAEiJx0iF/3W0TIsjTImj4AAAAOuDSYs8JEmJvCTgAAAA6+FmkIuH6AAAAIXAeAbDDx9EAABVBaCGAQBTSIn7SIPsCEiLL4mH6AAAAEiF7XQdSIu/4AAAAEiF/3QY6MP///8Dg+gAAACJg+gAAABIg8QIW13DSIu94AAAAEiF/3QcD76z2AAAAOhY/v//SImD4AAAAEiJx+vEDx9AAEiLfQBIhf90NOja/v//SInHSIXAdCwPvrXYAAAA6Cb+//9IiYXgAAAASInHSIX/dbNIiztIibvgAAAA64NIie/r8kiLfQBIib3gAAAA691mDx+EAAAAAABBV0GJ8UFWQVVBVFVTTInDSIPsGIXJD46aAAAASInWQYnKRTHbQbgBAAAADx9EAAAPtgZIidmEwHUV62IPH0AAD7ZGAUiDxgFIidGEwHRPg+hBSA++6EiLVOkISIXSdeBNY+BIg8YBQYPAAUyJ4kjB4gRMKeJIweIESAHaSIkKiILYAAAAx4LoAAAAYHn+/0iJVOkID7YGSInRhMB1sUGDwwGDgegAAAABSIPGAUU52g+Fev///0WFyQ+OlAIAAEGNQf9JifxFMe1MjXQHAesMSYPEAUEBxU055nRsQQ+2BCSD6EFID77oRA+++EiLROsISIXAdGpIicOLg+gAAACFwHnNTIs7BaCGAQCJg+gAAABNhf90ukiLq+AAAABIhe0PhPAAAACLhegAAACFwHhqA4PoAAAASYPEAYmD6AAAAEEBxU055nWUSIPEGESJ6FtdQVxBXUFeQV/DZg8fRAAASIsLSIXJdChIi5PgAAAASIXSD4TFAAAASItE6ghIhcB0XEiJROsISInD6Wr///+QSIlc6wjpX////0iLVQAFoIYBAImF6AAAAEiF0nSCTIu94AAAAE2F/w+EnQEAAEGLh+gAAACFwA+IRgEAAAOF6AAAAImF6AAAAOlS////TIsCTYXAD4QcAQAASIu64AAAAEiF/w+EiAEAAESJ/kiJVCQI6On7//9Ii1QkCEiJROoI6Wz///9Ji7/gAAAASIX/dEIPvrPYAAAA6ML7//9IiYPgAAAASInF6en+//9Ii7ngAAAASIX/dGMPvrPYAAAA6Jv7//9IiYPgAAAASInC6RT///9Jiz9Ihf8PhFABAADoG/z//0iJx0iFwA+EqgEAAEEPvrfYAAAA6GL7//9JiYfgAAAASInHSIX/dYVIiytIiavgAAAA6Xr+//9IizlIhf8PhBABAABIiUwkCOjO+///SItMJAhIhcBIiccPhHYBAAAPvrHYAAAA6BH7//9Ii0wkCEiJx0iJgeAAAABIhf8PhVL///9IixNIiZPgAAAA6XL+//9IiVTqCEiJ0Olv/v//TYsHBaCGAQBBiYfoAAAATYXAD4Si/v//SYu/4AAAAEiF/w+EHQEAAOjw+///QQOH6AAAAEGJh+gAAADpev7//0Ux7ent/f//SIu64AAAAEiF/3RpD7612AAAAOh9+v//SImF4AAAAEmJx+k8/v//TInHSIlUJAjoAfv//0iLVCQISIXASInHD4SaAAAAD76y2AAAAOhE+v//SItUJAhIicdIiYLgAAAA6Tr+//9Mif3p2P7//0iJyukq////SIs6SIX/D4S0AAAASIlUJAjoqvr//0iLVCQISIXASInHD4SNAAAAD76y2AAAAOjt+f//SItUJAhIicdIiYLgAAAASIX/D4VM////TIt9AEyJveAAAADpk/3//0mLP0mJv+AAAADpXv7//0iLOkiJuuAAAADpsf3//0iLOUiJueAAAADplv7//0yJx+gw+v//SInHSIXAdC1BD7632AAAAOh7+f//SYmH4AAAAEiJx+m3/v//SIs6SIm64AAAAOuCSYnX64pJiz9Jib/gAAAA6Zf+//9mLg8fhAAAAAAAZpDzDx76QVdMjT0rJgAAQVZJidZBVUmJ9UFUQYn8VUiNLRwmAABTTCn9SIPsCOjf9///SMH9A3QfMdsPH4AAAAAATInyTInuRInnQf8U30iDwwFIOd116kiDxAhbXUFcQV1BXkFfw2ZmLg8fhAAAAAAA8w8e+sM=')
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

string_match_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p)
string_match_c = ctypes.cast(code_address+0x1340-0x1020, string_match_type)

data = ctypes.create_string_buffer(DATA_SIZE)
data_address = ctypes.cast(data,ctypes.POINTER(ctypes.c_void_p))

NODE_SIZE=240
def string_match(dna, segments):
    dna_buf = dna.encode('utf-8')
    seg_buf = ('\0'.join(segments)+'\0').encode('utf-8')

    #We probably hava a lot of node overlap
    ctypes.memset(data_address, 0, min(DATA_SIZE, len(seg_buf)*NODE_SIZE))

    dna_len = len(dna_buf)
    seg_count = len(segments)

    return string_match_c(dna_buf, dna_len, seg_buf, seg_count, data_address)

highscore = False

dna = "ACTTACTGG"
segments = ["A", "ACT", "GG"]
print(string_match(dna, segments))
