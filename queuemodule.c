#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

#pragma GCC optimize ("align-functions=16")

void data_func();

#define front data[0]
#define back data[1]
#define max_size data[2]
#define array ((PyObject**)data+4)

#define _PyTuple_ITEMS(op) (_PyTuple_CAST(op)->ob_item)

int setCallAddress(PyObject *obj, void *address) {
  int offset = Py_TYPE(obj)->tp_vectorcall_offset;
  vectorcallfunc *func = (vectorcallfunc *)(((char *)obj) + offset);
  *func = address;
  return offset;
}

PyObject *make_superqu(PyObject *self, PyObject* args, PyObject* kwargs) {
  int offset = Py_TYPE(self)->tp_vectorcall_offset;
  vectorcallfunc func = *(vectorcallfunc *)(((char *)self) + offset);
  int *data = ((char*)func) + 0x400-0x60;

  front = args;
  back = front + 20;

  Py_INCREF(self);
  return self;
  
  /*  PyObject** stack = _PyTuple_ITEMS(args);
  PyObject *max_size_o = stack[0];

  

  max_size = 1234;//PyLong_AsLong(max_size_o);
  front = 0;
  back = 0;

  Py_INCREF(self);
  return self;*/
}

PyObject *superenqu(PyObject *self, PyObject* args, PyObject* kwargs) {
  PyObject** stack = _PyTuple_ITEMS(args);
  PyObject *item = stack[0];

  int offset = Py_TYPE(self)->tp_vectorcall_offset;
  vectorcallfunc func = *(vectorcallfunc *)(((char *)self) + offset);
  int *data = ((char*)func) + 0x400-0x130;

  Py_INCREF(item);
  array[back++ % max_size] = item;

  Py_INCREF(self);
  return self;
}

PyObject *superdequ(PyObject *self, PyObject* args, PyObject* kwargs) {
  int offset = Py_TYPE(self)->tp_vectorcall_offset;
  vectorcallfunc func = *(vectorcallfunc *)(((char *)self) + offset);
  int *data = ((char*)func) + 0x400-0x220;

  return array[front++ % max_size];
}
