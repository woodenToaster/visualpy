from functools import partial

import kivy
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

kivy.require('1.9.1')


class GraphicsManager(BoxLayout):
    frames = ListProperty([])

    def __init__(self, *args, **kwargs):
        self.orientation = 'vertical'
        super(GraphicsManager, self).__init__(*args, **kwargs)

    def add_frame(self, frame):
        self.frames.append(frame)

    def pop_frame(self):
        self.frames.pop()

    def render_frames(self):
        for frame in self.frames:
            self.render_frame(frame)

    def render_frame(self, frame):
        # self.draw_globals(frame)
        self.draw_locals(frame)

    def draw_globals(self, frame):
        print("Globals:")
        globs = globals()
        for var in globs:
            if var != '__builtins__':
                print("  {} = {}".format(var, globs.get(var, None)))

    def draw_locals(self, frame):
        for var in frame.f_code.co_varnames:
            self.add_widget(Label(text="  {} = {}".format(var, frame.f_locals.get(var, None))))

    def on_frames(self, instance, value):
        print("Frames: {}".format(instance.frames))
        print("Value: {}".format(value))


class VisualPyApp(App):

    def build(self):
        self.gm = GraphicsManager()
        btn = Button(text="Start")
        btn.bind(on_press=partial(self.vdb.runscript, self.script))
        self.gm.add_widget(btn)
        self.vdb.gm = self.gm
        return self.gm

    def run(self, vdb, script):
        self.vdb = vdb
        self.script = script
        super(VisualPyApp, self).run()
