import kivy
from kivy.app import App
from kivy.uix.label import Label

kivy.require('1.9.1')


class Frame(Label):
    pass
    # def update(self, *args, **kwargs)


class VisualPyApp(App):

    def build(self):
        return Frame(text="x=5")


if __name__ == '__main__':
    VisualPyApp().run()
