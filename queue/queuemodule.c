#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

#define front data[-2]
#define back data[-1]
#define array ((PyObject**)data)

#define PyCFunction_GET_FUNCTION(func)              \
  (((PyCFunctionObject *)func) -> m_ml -> ml_meth)

int setCallAddress(PyObject *obj, void *address) {
  PyCFunction_GET_FUNCTION(obj) = address;
  return 0;
}

int setMaxSize(int mx, PyObject* self, size_t* data) {
  front = 0;
  back = 0;
  *((size_t**)(self)+0x10) = data;
  return 0;
}

PyObject *superenqu(PyObject *self, PyObject* item) {
  size_t *data = *((size_t**)(self)+0x10);

  Py_INCREF(item);
  array[back++] = item;

  Py_INCREF(item);
  return item;
}

PyObject *superdequ(PyObject *self, PyObject* args) {
  size_t *data = *((size_t**)(self)+0x10);
  return array[front++];
}
