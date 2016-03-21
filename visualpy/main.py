import sys

from graphics import VisualPyApp
from vdb import Vdb

USAGE = """
Pass a python script as an argument to start visual execution.

$ python main.py my_script.py
"""


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(0)
    script = sys.argv[1]
    print("Tracing execution of " + script)
    trace_into = Vdb.get_funcs_in_script(script)
    _vdb = Vdb(trace_into)
    VisualPyApp().run(_vdb, script)

if __name__ == '__main__':
    main()
