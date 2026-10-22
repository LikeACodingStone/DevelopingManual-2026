#include <Python.h>
#include <stdio.h>
int main(void) {
    Py_Initialize();
    PyObject *module = PyImport_ImportModule("math");
    PyObject *fn = module ? PyObject_GetAttrString(module, "sqrt") : NULL;
    PyObject *arg = PyFloat_FromDouble(81.0);
    PyObject *result = fn && arg ? PyObject_CallOneArg(fn, arg) : NULL;
    int failed = result == NULL;
    if (!failed) {
        double value = PyFloat_AsDouble(result);
        failed = PyErr_Occurred() != NULL || value != 9.0;
        if (!failed) printf("sqrt=%.1f\n", value);
    }
    if (PyErr_Occurred()) PyErr_Print();
    Py_XDECREF(result); Py_XDECREF(arg); Py_XDECREF(fn); Py_XDECREF(module);
    if (Py_FinalizeEx() < 0) failed = 1;
    return failed;
}
