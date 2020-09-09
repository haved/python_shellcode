#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

#pragma GCC optimize ("align-functions=16")

void data_func();

#define front data[0]
#define back data[1]
#define max_size data[2]
#define array ((PyObject**)data+4)

int setCallAddress(PyObject *obj, void *address) {
  int offset = Py_TYPE(obj)->tp_vectorcall_offset;
  vectorcallfunc *func = (vectorcallfunc *)(((char *)obj) + offset);
  *func = address;
  return offset;
}

//args is a normal C array of object pointers
//nargsf is the amount, with a flag bit set sometimes
PyObject *make_superqu(PyObject *self, PyObject *const *args, size_t nargsf, PyObject *kwargs) {
  int offset = Py_TYPE(self)->tp_vectorcall_offset;
  vectorcallfunc func = *(vectorcallfunc *)(((char *)self) + offset);
  size_t *data = ((char*)func) + 0x400-0x60;

  //max_size is set using memmove
  front = 0;
  back = 0;

  Py_INCREF(self);
  return self;
}

PyObject *superenqu(PyObject *self, PyObject *const *args, size_t nargsf, PyObject *kwargs) {
  int offset = Py_TYPE(self)->tp_vectorcall_offset;
  vectorcallfunc func = *(vectorcallfunc *)(((char *)self) + offset);
  size_t *data = ((char*)func) + 0x400-0xe0;

  PyObject *item = args[0];

  Py_INCREF(item);
  array[back++ % max_size] = item;

  Py_INCREF(self);
  return self;
}

PyObject *superdequ(PyObject *self, PyObject *const *args, size_t nargsf, PyObject *kwargs) {
  int offset = Py_TYPE(self)->tp_vectorcall_offset;
  vectorcallfunc func = *(vectorcallfunc *)(((char *)self) + offset);
  size_t *data = ((char*)func) + 0x400-0x1a0;

  return array[front++ % max_size];
}
