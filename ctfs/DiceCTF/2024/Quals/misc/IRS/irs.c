#include "Python.h"

static int audit(const char *event, PyObject *args, void *userData) {
	static int running = 0;
	if (running) {
		exit(0);
	}
	if (!running && !strcmp(event, "exec")) running = 1;
	return 0;
}

static PyObject* irs_audit(PyObject *self, PyObject *args) {
	PySys_AddAuditHook(audit, NULL);
	Py_RETURN_NONE;
}

static PyMethodDef IrsMethods[] = {
	{"audit", irs_audit, METH_VARARGS, ""},
	{NULL, NULL, 0, NULL}
};

static PyModuleDef IrsModule = {
	PyModuleDef_HEAD_INIT, "irs", NULL, -1, IrsMethods,
	NULL, NULL, NULL, NULL
};

static PyObject* PyInit_Irs(void) {
	return PyModule_Create(&IrsModule);
}

int main(int argc, char **argv) {
	PyImport_AppendInittab("irs", &PyInit_Irs);
	return Py_BytesMain(argc, argv);
}
