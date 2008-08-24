#include <Python.h>
#include <limits.h>
#include <pygame/pygame.h>

#include "path.c"

typedef struct {
  PyObject_HEAD
  pathData *path;
  PyObject *overlay_holder[OVERLAYS];
} PathPathObject;

static int
path_init(PathPathObject *self, PyObject *args, PyObject *kwds)
{
  int w, h;
  if (!PyArg_ParseTuple(args, "(ii)", &w, &h))
    return -1;
  self->path = pathNew(w,h);
  if (self->path == NULL) {
    PyErr_SetString(PyExc_ValueError, "invalid dimensions");
    return -1;
  }
  return 0;
}

static PyObject *
path_set_map(PathPathObject *self, PyObject *args)
{
  int i;
  PySurfaceObject *x;
  if (!PyArg_ParseTuple(args, "iO!", &i, &PySurface_Type, &x))
    return NULL;
  if (i < 0 || i >= OVERLAYS) {
    PyErr_SetString(PyExc_ValueError, "invalid overlay");
    return NULL;
  }
  if (x->surf->w != self->path->width || x->surf->h != self->path->height) {
    PyErr_SetString(PyExc_ValueError, "invalid surface size");
    return NULL;
  }
  if (x->surf->format->BytesPerPixel != 1) {
    PyErr_SetString(PyExc_ValueError, "invalid surface mode");
    return NULL;
  }
  Py_XDECREF(self->overlay_holder[i]);
  self->overlay_holder[i] = x;
  Py_INCREF(x);
  pathSetOverlay(self->path, i, x->surf->pixels, 1);
  Py_RETURN_NONE;
}


static PyObject *
path_get_path(PathPathObject *self, PyObject *args) {
  int startx, starty, starthead, destx, desty;
  int *result;
  if (!PyArg_ParseTuple(args, "(ii)i(ii)", &startx, &starty, &starthead, &destx, &desty))
    return NULL;
  Py_BEGIN_ALLOW_THREADS
  result = pathFind(self->path,startx,starty,starthead,destx,desty);
  Py_END_ALLOW_THREADS
  if (result == NULL) Py_RETURN_NONE;
  PyObject *list = PyList_New(0);
  int i;
  for (i = 2; i < (result[0]*2+2); i += 2)
    PyList_Append(list, Py_BuildValue("(ii)",result[i],result[i+1]));
  free(result);
  Py_INCREF(list);
  return list;
}

static PyMethodDef path_methods[] = {
  {"get_path", (PyCFunction)path_get_path, METH_VARARGS, NULL},
  {"set_map", (PyCFunction)path_set_map, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}
};

static PyObject *
path_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
        PyObject *new;

        new = type->tp_alloc(type, 0);
        if (new != NULL) {
        }
        return new;
}

static void
path_dealloc(PathPathObject *p)
{
  pathFree(p->path);
  p->ob_type->tp_free((PyObject *)p);
}

static PyTypeObject path_type = {
        PyObject_HEAD_INIT(0)   /* Must fill in type value later */
        0,                                      /* ob_size */
        "path.path",                            /* tp_name */
        sizeof(PathPathObject),                 /* tp_basicsize */
        0,                                      /* tp_itemsize */
        (destructor)path_dealloc,               /* tp_dealloc */
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
        path_methods,                           /* tp_methods */
        0,                        /* tp_members */
        0,                                      /* tp_getset */
        0,                                      /* tp_base */
        0,                                      /* tp_dict */
        0,                                      /* tp_descr_get */
        0,                                      /* tp_descr_set */
        0,                                      /* tp_dictoffset */
        (initproc) path_init,                           /* tp_init */
        PyType_GenericAlloc,                    /* tp_alloc */
        path_new,                               /* tp_new */
        PyObject_Del,                           /* tp_free */
};


PyMODINIT_FUNC
initpath(void)
{
  PyObject *m;
  m = Py_InitModule("path", NULL);
  if (m == NULL)
    return;
  import_pygame_surface();
  path_type.ob_type = &PyType_Type;
  if (PyType_Ready(&path_type) < 0)
    return;
  Py_INCREF(&path_type);
  PyModule_AddObject(m, "path", (PyObject *)&path_type);
}
