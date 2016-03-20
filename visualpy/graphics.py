class GraphicsManager():

    def __init__(self):
        self.frames = []

    def add_frame(self, frame):
        self.frames.append(frame)

    def pop_frame(self):
        self.frames.pop()

    def render_frames(self):
        for frame in self.frames:
            self.render_frame(frame)

    def render_frame(self, frame):
        self.draw_globals(frame)
        self.draw_locals(frame)

    def draw_globals(self, frame):
        print("Globals:")
        globs = globals()
        for var in globs:
            if var != '__builtins__':
                print("  {} = {}".format(var, globs.get(var, None)))

    def draw_locals(self, frame):
        print("Locals:")
        for var in frame.f_code.co_varnames:
            print("  {} = {}".format(var, frame.f_locals.get(var, None)))
