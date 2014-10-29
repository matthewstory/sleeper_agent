import sleeper_agent
import unittest
import re

try:
    unittest.TestCase.assertIn
except AttributeError:
    import unittest2 as unittest

# WARNING: some assertions depend on specific line numbers in this
#          file. Please take care when updating the test cases.


class SleeperAgentFooObject(object):
    pattern = r"\n\s*[0-9.]+ b\s*1 object\s* <class '[^']*SleeperAgentFooObject'>\n"


class SleeperAgentBarObject(object):
    pattern = r"\n\s*[0-9.]+ b\s*1 object\s* <class '[^']*SleeperAgentBarObject'>\n"


class SleeperAgentSmokeTest(unittest.TestCase):
    "Basic tests that the functions can be called and don't return garbage."

    def test_python__get_state_info(self):
        "_get_state_info() should return something sane."
        state_info = sleeper_agent._get_state_info()
        self.assertIn("test_python__get_state_info", state_info)
        self.assertIn('test.py", line 27', state_info)
        self.assertNotIn("test_c_sleeper_agent_state", state_info)
        self.assertNotIn('test.py", line 36', state_info)


    def test_c_sleeper_agent_state(self):
        "C extension's sleeper_agent_state() should return something sane."
        state_info = sleeper_agent._sleeper_agent_activation.sleeper_agent_state()
        self.assertIn("test_c_sleeper_agent_state", state_info)
        self.assertIn('test.py", line 36', state_info)
        self.assertNotIn("test_python__get_state_info", state_info)
        self.assertNotIn('test.py", line 27', state_info)

    def _test_get_mem_info(self, method):
        "_get_mem_info() methods should return something sane."
        foo = SleeperAgentFooObject()
        mem_info = method()
        assert mem_info.startswith("### Memory Usage"), 'Memery report header works'
        assert re.search(SleeperAgentFooObject.pattern, mem_info), \
               "foo is in memory report"
        assert re.search(SleeperAgentBarObject.pattern, mem_info) is None, \
               "no SleeperAgentBarObject's should be in the report"

    def test_python__get_mem_info(self):
        "_get_mem_info() should return something sane."
        self._test_get_mem_info(sleeper_agent._get_mem_info)

    def test_python__get_mem_info(self):
        "C extension's sleeper_agent_memstate() should return something sane."
        self._test_get_mem_info(sleeper_agent._sleeper_agent_activation.sleeper_agent_memstate)

    def test_python_and_c_functions_return_same_string(self):
        "_get_state_info() and sleeper_agent_state() should return the same value."
        # WARNING: the two function calls should be on the same line,
        #          otherwise they won't match.
        # WARNING: the memory report cannot pass this test, as more objects
        #          are created during the C call, changing the report details
        py_bt, c_bt = \
               sleeper_agent._get_state_info(), sleeper_agent._sleeper_agent_activation.sleeper_agent_state()
        self.assertEqual(py_bt, c_bt)
