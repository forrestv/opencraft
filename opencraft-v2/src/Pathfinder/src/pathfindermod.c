#include <Python.h>
#include <limits.h>

#include "pathfinder.c"

typedef struct {
  PyObject_HEAD
  pathfinderData *path;
} PathfinderObject;

static int
pathfinder_init(PathfinderObject *self, PyObject *args, PyObject *kwds)
{
  int w, h;
  if (!PyArg_ParseTuple(args, "(ii)", &w, &h))
    return -1;
  self->path = pathfinderNew(w,h);
  if (self->path == NULL) {
    PyErr_SetString(PyExc_ValueError, "invalid dimensions");
    return -1;
  }
  return 0;
}

static PyObject *
pathfinder_overlay(PathfinderObject *self, PyObject *args)
{
  int x;
  if (!PyArg_ParseTuple(args, "z#", &self->path->overlay[0], &x))
    return NULL;
/*
  PyObject *newmap;
  
  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &newmap))
    return NULL;

  int h = PyList_Size(newmap);
  if (h != self->h) {
    PyErr_SetString(PyExc_ValueError, "bad map");
    return NULL;
  }
  int w = PyList_Size(PyList_GetItem(newmap,0));
  if (w != self->w) {
    PyErr_SetString(PyExc_ValueError, "bad map");
    return NULL;
  }
  int i,j;
  PyObject *line, *item;
  
  for (i = 0; i < h; i++) {
    line = PyList_GetItem(newmap,i);
    if (!PyList_Check(line) || PyList_Size(line) != w) {
      PyErr_SetString(PyExc_ValueError, "bad map");
      return NULL;
    }
    for (j = 0; j < w; j++) {
      item = PyList_GetItem(line,j);
      if (!PyInt_Check(item)) {
        PyErr_SetString(PyExc_ValueError, "bad map");
        return NULL;
      }
    }
  }
  if (self->map) {
    Py_DECREF(self->map);
  }
  Py_INCREF(newmap);
  self->map = newmap; */
  Py_RETURN_NONE;
}


static PyObject *
pathfinder_find(PathfinderObject *self, PyObject *args) {
  int startx, starty, starthead, destx, desty;
  if (!PyArg_ParseTuple(args, "(ii)i(ii)", &startx, &starty, &starthead, &destx, &desty))
    return NULL;
  int *result = pathfinderFind(self->path,startx,starty,starthead,destx,desty);
  if (result == NULL) Py_RETURN_NONE;
  PyObject *list = PyList_New(0);
  int i;
  for (i = 2; i < (result[0]*2+2); i += 2)
    PyList_Append(list, Py_BuildValue("(ii)",result[i],result[i+1]));

  Py_INCREF(list);
  return list;
}

static PyMethodDef pathfinder_methods[] = {
  {"overlay", (PyCFunction)pathfinder_overlay, METH_VARARGS, NULL},
  {"find", (PyCFunction)pathfinder_find, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}
};

static PyObject *
pathfinder_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
        PyObject *new;

        new = type->tp_alloc(type, 0);
        if (new != NULL) {
        }
        return new;
}

static void
pathfinder_dealloc(PathfinderObject *p)
{
  if (p->path)
    pathfinderFree(p->path);
  p->ob_type->tp_free((PyObject *)p);
}

static PyTypeObject pathfinder_type = {
        PyObject_HEAD_INIT(0)   /* Must fill in type value later */
        0,                                      /* ob_size */
        "pathfinder.pathfinder",                /* tp_name */
        sizeof(PathfinderObject),                 /* tp_basicsize */
        0,                                      /* tp_itemsize */
        (destructor)pathfinder_dealloc,               /* tp_dealloc */
        0,                                      /* tp_print */
        0,                                      /* tp_getattr */
        0,                                      /* tp_setattr */
        0,                                      /* tp_compare */
        0,                                      /* tp_repr */
        0,                                      /* tp_as_number */
        0,                                      /* tp_as_sequence */
        0,                                      /* tp_as_mapping */
        0,                                      /* tp_hash */
        0,                                      /* tp_call */
        0,                                      /* tp_str */
        0,                /* tp_getattro */
        0,                                      /* tp_setattro */
        0,                                      /* tp_as_buffer */
        Py_TPFLAGS_DEFAULT, /* tp_flags */
        0,                                      /* tp_doc */
        0,                                      /* tp_traverse */
        0,                                      /* tp_clear */
        0,                                      /* tp_richcompare */
        0,                                      /* tp_weaklistoffset */
        0,                                      /* tp_iter */
        0,                                      /* tp_iternext */
        pathfinder_methods,                           /* tp_methods */
        0,                        /* tp_members */
        0,                                      /* tp_getset */
        0,                                      /* tp_base */
        0,                                      /* tp_dict */
        0,                                      /* tp_descr_get */
        0,                                      /* tp_descr_set */
        0,                                      /* tp_dictoffset */
        (initproc) pathfinder_init,                           /* tp_init */
        PyType_GenericAlloc,                    /* tp_alloc */
        pathfinder_new,                               /* tp_new */
        PyObject_Del,                           /* tp_free */
};


PyMODINIT_FUNC
initPathfinder(void)
{
  PyObject *m;
  m = Py_InitModule("Pathfinder", NULL);
  if (m == NULL)
    return;
  
  pathfinder_type.ob_type = &PyType_Type;
  if (PyType_Ready(&pathfinder_type) < 0)
    return;
  Py_INCREF(&pathfinder_type);
  PyModule_AddObject(m, "Pathfinder", (PyObject *)&pathfinder_type);
}
