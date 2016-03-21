import kivy
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.uix.label import Label
from kivy.uix.widget import Widget

kivy.require('1.9.1')


class GraphicsManager(Widget):

    def __init__(self):
        self.frames = []
        self.fud = FrameUpdateDispatcher()

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

    def on_frames_update_callback(self):
        print("Callback called from GraphicsManager")


class FrameUpdateDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_frame_update')
        super(FrameUpdateDispatcher, self).__init__(**kwargs)

        def on_frame_update(self, *args):
            print("Updating frame graphics in FrameUpdateDispatcher")


class VisualPyApp(App):

    def build(self):
        return Label(text="x=5")

    def run(self, vdb, script):
        self.vdb = vdb
        self.script = script
        super(VisualPyApp, self).run()
