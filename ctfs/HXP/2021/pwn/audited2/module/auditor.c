#define PY_SSIZE_T_CLEAN

#include <stdatomic.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdnoreturn.h>
#include <string.h>
#include <sys/syscall.h>

#include <Python.h>

static atomic_bool auditor_may_exec = ATOMIC_VAR_INIT(false);
static atomic_flag auditor_did_exec = ATOMIC_FLAG_INIT;

noreturn static void auditor_exit(int status)
{
    for (;;) // Under no circumstances whatsoever continue running.
        __asm__ volatile ( "syscall" :: "a"(SYS_exit_group), "D"(status) );
}

static int auditor_hook(const char *event, PyObject *Py_UNUSED(args), void *Py_UNUSED(user_data))
{
    // You get _one_ free call to auditor.exec. That's it.
    if (!atomic_load(&auditor_may_exec) || atomic_flag_test_and_set(&auditor_did_exec) || strcmp(event, "exec"))
        auditor_exit(EXIT_FAILURE);
    return 0;
}

static PyObject *auditor_activate(PyObject *Py_UNUSED(module), PyObject *Py_UNUSED(args))
{
    if (PySys_AddAuditHook(auditor_hook, NULL) != 0)
        auditor_exit(EXIT_FAILURE);
    Py_RETURN_NONE;
}

static PyObject *auditor_exec(PyObject *Py_UNUSED(module), PyObject *args)
{
    PyObject *builtins = PyEval_GetBuiltins();
    PyObject *exec = PyDict_GetItemString(builtins, "exec");
    atomic_store(&auditor_may_exec, true);
    PyObject_CallObject(exec, args);
    atomic_store(&auditor_may_exec, false);
    // No cleanup necessary - we tear down the entire process instead!
    auditor_exit(EXIT_SUCCESS);
}

static PyMethodDef auditor_methods[] = {
    { "activate", (PyCFunction) auditor_activate, METH_NOARGS, "Activate the auditor" },
    { "exec", (PyCFunction) auditor_exec, METH_VARARGS, "Execute code like Python's builtin exec, then exit." },
    { NULL }
};

static PyModuleDef auditor_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "auditor",
    .m_doc = "More auditing!",
    .m_size = -1,
    .m_methods = auditor_methods
};

PyMODINIT_FUNC PyInit_auditor(void)
{
    return PyModule_Create(&auditor_module);
}
