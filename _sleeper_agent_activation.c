#include <Python.h>

/* Return result of sleeper_agent._get_state_info() as a C string */
static char *
get_state(char *attr)
{
     char *rv = NULL;
     PyGILState_STATE gstate;

     gstate = PyGILState_Ensure();
     rv = PyString_AsString(
          PyObject_Call(
               PyObject_GetAttrString(
                    PyImport_ImportModule("sleeper_agent"),
                    attr),
               Py_BuildValue("()"), NULL));
     PyGILState_Release(gstate);

     return rv;
}

char * sleeper_agent_state(void)
{
	return get_state("_get_state_info");
}
char * sleeper_agent_memstate(void)
{
	return get_state("_get_mem_info");
}


/* Return sleeper_agent_state() as Python string, for testing and fun */
static PyObject *
sleeper_agent_state_pyobject(PyObject *self, PyObject *args)
{
     return Py_BuildValue("s", sleeper_agent_state());
}

static PyObject *
sleeper_agent_memstate_pyobject(PyObject *self, PyObject *args)
{
     return Py_BuildValue("s", sleeper_agent_memstate());
}

static PyMethodDef SleeperAgentMethods[] = {
     {"sleeper_agent_state",  sleeper_agent_state_pyobject, METH_VARARGS,
      "Return the sleeper agent state as a Python string."},
	 {"sleeper_agent_memstate", sleeper_agent_memstate_pyobject, METH_VARARGS,
	  "Return the sleeper agent memory state as a Python string."},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
init_sleeper_agent_activation(void)
{
     (void) Py_InitModule("_sleeper_agent_activation", SleeperAgentMethods);
}
