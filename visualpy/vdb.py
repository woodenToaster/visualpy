import bdb
import cmd
import re


class Vdb(bdb.Bdb, cmd.Cmd):

    def __init__(self, trace, completekey='tab', stdin=None, stdout=None, skip=None):
        bdb.Bdb.__init__(self, skip=skip)
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        self.trace_into = trace
        self.gm = None

    @staticmethod
    def get_funcs_in_script(script):
        """Return a list of all function names in the given script.

        :param script: The script to examine. This can be a filename or
                       the script itself
        :type script: str
        :returns: List of function names found in the script
        """
        funcs = []
        func_regex = r'^\s*def ([\w_]+)\('
        if script.endswith('.py'):
            with open(script, 'r') as fp:
                lines = fp.readlines()
        else:
            lines = script.split('\n')
        for line in lines:
            match = re.search(func_regex, line)
            if match:
                funcs.append(match.group(1))
        return funcs

    def trace_dispatch(self, frame, event, arg):
        if self.quitting:
            return
        if event == 'line':
            return self.trace_lines(frame)
        if event == 'call':
            return self.trace_calls(frame, arg)
        if event == 'return':
            return self.trace_returns(frame, arg)
        if event == 'exception':
            return self.trace_exceptions(frame, arg)
        if event == 'c_call':
            return self.trace_dispatch
        if event == 'c_exception':
            return self.trace_dispatch
        if event == 'c_return':
            return self.trace_dispatch
        print('bdb.Bdb.dispatch: unknown debugging event:', repr(event))
        return self.trace_dispatch

    def trace_lines(self, frame):
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        print("  {} line {}".format(func_name, line_no))
        self.gm.render_frames()

    def trace_calls(self, frame, arg):
        co = frame.f_code
        func_name = co.co_name
        if func_name not in self.trace_into:
            return
        print("Entered function {}".format(func_name))
        self.gm.add_frame(frame)
        return self.trace_dispatch

    def trace_returns(self, frame, arg):
        print("Exiting from {}".format(frame.f_code.co_name))
        self.gm.pop_frame()
        return self.trace_dispatch

    def trace_exceptions(self, frame):
        print("Exception thrown")

    def runscript(self, script_name, _):
        import __main__
        __main__.__dict__.clear()
        __main__.__dict__.update(
            {
                '__name__': '__main__',
                '__file__': script_name,
                '__builtins__': __builtins__
            }
        )
        self.mainpyfile = self.canonic(script_name)

        with open(script_name, 'r') as fp:
            stmt_fmt = "exec(compile({}, {}, 'exec'))"
            statement = stmt_fmt.format(repr(fp.read()), repr(self.mainpyfile))
        self.run(statement)
