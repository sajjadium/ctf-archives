from pyglet.graphics import Batch
from pyglet.gui import Frame
from pyglet.window import Window

from client.game.ui.dialog import Dialog, DialogCallback
from client.scenes.scenemanager import Scene


class DialogScene(Scene):
    def __init__(
        self,
        window: Window,
    ) -> None:
        super().__init__(window=window)

        self.batch = Batch()
        self.frame = Frame(window=window)

        self.dialog = Dialog(
            0,
            0,
            self.window.width,
            200,
            [],
            batch=self.batch,
        )

    def draw(self) -> None:
        self.dialog.draw()
        self.batch.draw()

        return super().draw()

    @property
    def callback(self) -> DialogCallback:
        return self.dialog.cb

    @callback.setter
    def callback(self, cb: DialogCallback) -> None:
        self.dialog.cb = cb

    def append_text(self, text: str) -> None:
        self.dialog.append_text(text)

    def set_text(self, text: list[str]) -> None:
        self.dialog.text = text

    def next_text(self) -> None:
        self.dialog.next_text()

    def activate(self) -> None:
        self.frame.add_widget(widget=self.dialog)

        self.dialog.start(self.dialog.text, self.callback)

    def deactivate(self) -> None:
        self.cb = None

        self.frame.remove_widget(widget=self.dialog)
        self.dialog.stop()
