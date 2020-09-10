#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

#define front data[-3]
#define back data[-2]
#define max_size data[-1]
#define array ((PyObject**)data)

#pragma GCC optimize ("align-functions=16")

#define PyCFunction_GET_FUNCTION(func)              \
  (((PyCFunctionObject *)func) -> m_ml -> ml_meth)

int setCallAddress(PyObject *obj, void *address) {
  PyCFunction_GET_FUNCTION(obj) = address;
  return 0;
}

int setMaxSize(int mx, PyObject* self, size_t* data) {
  front = 0;
  back = 0;
  max_size = mx;
  *((size_t**)(self)+0x10) = data;
  return 0;
}

PyObject *superenqu(PyObject *self, PyObject* item) {
  size_t *data = *((size_t**)(self)+0x10);

  Py_INCREF(item);
  array[back++ % max_size] = item;

  Py_INCREF(item);
  return item;
}

PyObject *superdequ(PyObject *self, PyObject* item) {
  size_t *data = *((size_t**)(self)+0x10);
  return array[front++ % max_size];
}
