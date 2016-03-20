import os
import sys

import cutest as unittest

abs_test_path = os.path.abspath(os.path.dirname(__file__))
top_level_dir = os.path.join(abs_test_path, '..')
module_dir = os.path.join(top_level_dir, 'visualpy')
sys.path.extend([top_level_dir, module_dir])
from visualpy.vdb import Vdb


class TestHelpers(unittest.TestCase):

    def test_get_funcs_in_script_from_file(self):
        test_script = os.path.join(abs_test_path, 'test_simple.py')
        funcs = Vdb.get_funcs_in_script(test_script)
        self.assertListEqual(funcs, ['test_variables', 'another_func'])

    def test_get_funcs_in_script_from_string(self):
        test_script = """
        def test_variables(arg_one):
            x = arg_one
            y = arg_one
            z = x + y

            def another_func(z):
                print(z)
            another_func(z)

        test_variables(6)
        """
        funcs = Vdb.get_funcs_in_script(test_script)
        self.assertListEqual(funcs, ['test_variables', 'another_func'])

if __name__ == '__main__':
    unittest.main()
