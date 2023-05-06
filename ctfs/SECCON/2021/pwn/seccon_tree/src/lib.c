#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

static PyTypeObject TreeType;

typedef long long int lli;
typedef struct {
    PyObject_HEAD
    PyObject *object;
    PyObject *left;
    PyObject *right;
} Tree;


static void
Tree_dealloc(Tree *self)
{
    Py_XDECREF(self->left);
    Py_XDECREF(self->right);
    Py_XDECREF(self->object);

    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
Tree_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *obj;
    if (!PyArg_ParseTuple(args, "O", &obj)) {
        return NULL;
    }

    Tree* self = (Tree *)type->tp_alloc(type, 0);
    if (self == NULL) {
        return NULL;
    }

    Py_INCREF(obj);
    self->object = obj;

    return (PyObject *)self;
}

static PyObject*
add_child_left(Tree *self, PyObject *args) {
    PyObject *obj;
    if (!PyArg_ParseTuple(args, "O!", &TreeType, &obj)) {
        return NULL;
    }
    if (self->left != NULL) {
        Py_DECREF(self->left);
    }
    Py_INCREF(obj);
    self->left = obj;

    Py_RETURN_NONE;
}

static PyObject*
add_child_right(Tree *self, PyObject *args) {
    PyObject *obj;
    if (!PyArg_ParseTuple(args, "O!", &TreeType, &obj)) {
        return NULL;
    }
    if (self->right != NULL) {
        Py_DECREF(self->right);
    }
    Py_INCREF(obj);
    self->right = obj;

    Py_RETURN_NONE;
}

static PyObject*
get_child_left(Tree *self, PyObject *args) {
    PyObject *obj;
    if (!PyArg_ParseTuple(args, "")) {
        return NULL;
    }
    if (self->left == NULL) {
        Py_RETURN_NONE;
    } else {
        obj = self->left;
        Py_INCREF(obj);
        return (PyObject*)obj;
    }
}

static PyObject*
get_child_right(Tree *self, PyObject *args) {
    PyObject *obj;
    if (!PyArg_ParseTuple(args, "")) {
        return NULL;
    }
    if (self->right == NULL) {
        Py_RETURN_NONE;
    } else {
        obj = self->right;
        Py_INCREF(obj);
        return (PyObject*)obj;
    }
}

Tree* find_node_inner(Tree *self, const char *key) {
    Tree* result = NULL;

    PyObject* rpr = PyObject_Repr(self->object);
    if (rpr == NULL) {
        return NULL;
    }
    const char *label = PyUnicode_AsUTF8(rpr);
    if (label == NULL) {
        Py_DECREF(rpr);
        return NULL;
    }
    if (strcmp(label, key) == 0) {
        result = (Tree *)self;
    }
    Py_DECREF(rpr);

    if (result == NULL && self->left != NULL) {
        result = find_node_inner((Tree*)self->left, key);
    }
    if (result == NULL && self->right != NULL) {
        result = find_node_inner((Tree*)self->right, key);
    }

    return result;
}

static PyObject*
find_node(Tree *self, PyObject *args) {
    PyObject *obj;
    if (!PyArg_ParseTuple(args, "O", &obj)) {
        return NULL;
    }

    PyObject* rpr = PyObject_Repr(obj);
    if (rpr == NULL) {
        return NULL;
    }
    const char *s = PyUnicode_AsUTF8(rpr);
    if (s == NULL) {
        Py_DECREF(rpr);
        return NULL;
    }
    PyObject* result = (PyObject*)find_node_inner(self, s);
    Py_DECREF(rpr);

    if (result != NULL) {
        Py_INCREF(result);
        return result;
    }
    Py_RETURN_NONE;
}

static PyObject*
get_object(Tree *self, PyObject *args) {
    if (!PyArg_ParseTuple(args, "")) {
        return NULL;
    }
    PyObject *obj = self->object;
    Py_INCREF(obj);
    return obj;
}

static PyMethodDef TreeMethods[] = {
    {"find", (PyCFunction)find_node, METH_VARARGS, "tree: find"},
    {"get_object", (PyCFunction)get_object, METH_VARARGS, "tree: get_object"},
    {"get_child_left", (PyCFunction)get_child_left, METH_VARARGS, "tree: get_child_left"},
    {"get_child_right", (PyCFunction)get_child_right, METH_VARARGS, "tree: get_child_right"},
    {"add_child_left", (PyCFunction)add_child_left, METH_VARARGS, "tree: add_child_left"},
    {"add_child_right", (PyCFunction)add_child_right, METH_VARARGS, "tree: add_child_right"},
    {NULL}
};

static PyTypeObject TreeType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "seccon_tree.Tree",             /* tp_name */
    sizeof(Tree),                   /* tp_basicsize */
    0,                              /* tp_itemsize */
    (destructor)Tree_dealloc,       /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_reserved */
    0,                              /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    0,                              /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,             /* tp_flags */
    "my tree",                      /* tp_doc */
    0,                              /* tp_traverse */
    0,                              /* tp_clear */
    0,                              /* tp_richcompare */
    0,                              /* tp_weaklistoffset */
    0,                              /* tp_iter */
    0,                              /* tp_iternext */
    TreeMethods,                    /* tp_methods */
    0,                              /* tp_members */
    0,                              /* tp_getset */
    0,                              /* tp_base */
    0,                              /* tp_dict */
    0,                              /* tp_descr_get */
    0,                              /* tp_descr_set */
    0,                              /* tp_dictoffset */
    0,                              /* tp_init */
    0,                              /* tp_alloc */
    Tree_new,                       /* tp_new */
};


static struct PyModuleDef tree_module = {
    PyModuleDef_HEAD_INIT,
    "seccon_tree",
    NULL,
    -1,
};

PyMODINIT_FUNC PyInit_seccon_tree (void) {
    PyObject *m;
    if (PyType_Ready(&TreeType) < 0)
        return NULL;
    m = PyModule_Create(&tree_module);
    if (m == NULL)
        return NULL;
    Py_INCREF(&TreeType);

    if (PyModule_AddObject(m, "Tree", (PyObject *) &TreeType) < 0) {
        Py_DECREF(&TreeType);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}
