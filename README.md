# Python shellcode

This repository contains my attempts at running C in python for extra speed,
in a setting where one is only allowed to submit a single python file.

I am running Linux, and the target server is as well.
I have no idea how this would be on Windows, but you probably don't get `mmap` from `libc`.

## Running machine code in Python
This is accomplished through allocating a block of memory using `mmap`,
accessed through the python library `ctypes`.
```python
libc = ctypes.cdll.LoadLibrary(None) # Gives libc
mmap_function = libc.mmap
mmap_function.restype = ctypes.c_void_p
mmap_function.argtypes = (ctypes.c_void_p, ctypes.c_size_t,
                          ctypes.c_int, ctypes.c_int,
                          ctypes.c_int, ctypes.c_size_t)
CODE_SIZE = 1000
code_address = mmap_function(None, CODE_SIZE,
                             mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC,
                             mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS,
                             -1, 0)
if code_address == -1:
    raise OSError('mmap failed to allocate memory')
```

The memory is marked as both writeable and executable,
so we can copy whatever bytes we feel like to the block.
If the block happens to contain machinecode, we can cast the address of the machinecode
into a ctypes function pointer with the correct signature, and call the function.

## Compiling C to machine code
In this case, the block of machinecode comes from a C-program with the following function:
```c
int cuboid(int n, int* heights, int* data) {
   ...
```

The c program `pool.c` has been compiled using
```
gcc -O3 -c pool.c -o pool.o
```
This creates an object file containing machine code for the function, but it will not be linked with anything.
This means function calls don't work from one function to another,
and standard libraries / Python libraries are not accessible.
You can probably hack around this, but I recommend using macros for most things.

You can not use global variables either, but local variables work fine.
Keep in mind that string literals might be lost when copying the `.text` section.
My general tip is to pass a common data pointer as a parameter to every function.

## Exporting machine code to python
After compiling, check at what offsets of `.text` your function(s) start at.
```
objdump -d -M intel pool.o
```

Now dump the text section into it's own file `text.o` (without ELF headers or anything, just pure machinecode)
```
objcopy --only-section=.text -O binary pool.o text.o
```

Finally use some python to turn the binary file (`text.o`) into a python byte literal (`text.py`).
```python
with open("text.o", "rb") as fil:
    with open("text.py", "w") as ut:
        ut.write(str(fil.read()))
```

Now this block of machinecode bytes can be copied into our mmapped block,
and the address of the function *inside* the block can be casted to a ctypes function pointer.

```python
code=b'<machine code here>'
assert len(code) <= CODE_SIZE
ctypes.memmove(code_address, code, len(code))

cuboid_function_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
cuboid_function = ctypes.cast(code_address+0x00, cuboid_function_type)
```

Now we can call `cuboid_function` as a regular python function that takes three numbers, and returns an int.
`ctypes` will handle converting python types to C values of correct size.

## Allocating working memory
Our call to mmap takes a size, but is not guarranteed to be of that size.
If you need a big block of working memory, I suggest using
```
data_address = ctypes.cast(ctypes.create_string_buffer(DATA_SIZE),ctypes.POINTER(ctypes.c_void_p))
```
This will allocate a buffer of size `DATA_SIZE` bytes, and cast it to a void pointer.
This value can now be passed to any function that takes a `int* data`, or whatever other
pointer type you want.

## Passing arrays from python to C
The way I did this was by creating an `array.array('i')`, and appending all the needed data.
To pass it to a C function I simply get the address and pass it as a void pointer. (recieved as an `int*`).
```
array_address, _ = heights.buffer_info()
```

## Removing ctypes overhead
ctypes does conversions and stuff, which makes it kind of slow.
If you're calling the ctypes function once or twice that's fine,
but if you want to call it 1000 times it might not even be faster than writing
your solution in python.

My trick for this is using ctypes a constant number of times to change the internal function pointers of
some arbitrary python builtins, and then calling those. This is however much harder,
since one must compile with the correct version of the `Python.h` header to access internal fields,
and you can not use function calls, only macros (and static (?)). You need to work with `PyObject*`
everywhere since that's the signatures of the internal python functions you impersonate.
This also means reference counting counts on you to increase references of stuff.

To see this, go to the [queue readme](queue/readme.md).
