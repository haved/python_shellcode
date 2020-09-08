#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

#define max_size data[-1]
#define front data[-2]
#define tail data[-3]

int* getData() {

}

int* setCallAddress(PyObject *obj, size_t address) {
  Py_TYPE(obj)->tp_call = address;
  void* data;
  asm("call 5;"
      "pop %0;"
      :"=r"(data)
      :
      :
      );
  return data;
}

PyObject *make_superqu(PyObject *self, PyObject* args, PyObject* kwargs) {

  PyObject *max_size_o = ((PyTupleObject *)args) -> ob_item[0];

  /*int* data = getData();
  max_size = PyLong_AsLong(max_size_o);*/

  Py_INCREF(self);
  return self;
}
