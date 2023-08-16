from pyglet.graphics import Batch
from pyglet.gui import Frame
from pyglet.window import Window

from client.game.ui.button import TextButton
from client.game.ui.dialog import Dialog
from client.game.ui.dropdown import Dropdown
from client.game.ui.input import PasswordInput
from client.scenes.scenemanager import Scene


class TestScene(Scene):
    def __init__(self, window: Window):
        self.frame = Frame(window, order=4)
        self.batch = Batch()
        self._text_button = TextButton("ASDFKKKk", x=100, y=100, batch=self.batch)
        self._text_button.set_handler("on_press", lambda: None)

        self._dropdown = Dropdown(
            x=200, y=200, entries=["A", "B", "CCC"], batch=self.batch
        )

        self._dialog = Dialog(
            400,
            200,
            400,
            200,
            text=[
                "Hello World.",
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
                "123",
            ],
            batch=self.batch,
        )

        def text_entry_handler(text: str) -> None:
            print(text)

        self._input = PasswordInput(
            "value",
            500,
            100,
            200,
            batch=self.batch,
            text_color=(255, 0, 0, 255),
            caret_color=(0, 0, 0, 255),
            color=(0, 0, 0, 0),
        )
        self._input.set_handler("on_commit", text_entry_handler)

    def activate(self) -> None:
        self.frame.add_widget(self._input)
        self.frame.add_widget(widget=self._dialog)
        self.frame.add_widget(self._dropdown)
        self.frame.add_widget(self._text_button)

        super().activate()

    def deactivate(self) -> None:
        self.frame.remove_widget(self._input)
        self.frame.remove_widget(widget=self._dialog)
        self.frame.remove_widget(self._dropdown)
        self.frame.remove_widget(self._text_button)

        super().deactivate()

    def draw(self):
        self._text_button.draw()
        self._dialog.draw()
        self._input.draw()
        self.batch.draw()
