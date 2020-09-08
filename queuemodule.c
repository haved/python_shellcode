#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

void front();
void back();
void max_size();
void array();

int* setCallAddress(PyObject *obj, size_t address) {
  Py_TYPE(obj)->tp_call = address;
  return front;
}

PyObject *make_superqu(PyObject *self, PyObject* args, PyObject* kwargs) {
  PyObject *max_size_o = ((PyTupleObject *)args) -> ob_item[0];

  /*int* data = getData();
  max_size = PyLong_AsLong(max_size_o);*/

  Py_INCREF(self);
  return self;
}

void front() {
  
}

void back() {
  
}

void max_size() {
  
}

void array() {
  
}
