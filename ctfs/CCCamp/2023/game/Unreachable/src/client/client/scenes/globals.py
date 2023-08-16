from pyglet.text import Label
from pyglet.window import FPSDisplay, Window

from client.scenes.scenemanager import Scene
from shared.gen.messages.v1 import Error, ErrorType


class Globals(Scene):
    error_message: str

    def __init__(self, window: Window) -> None:
        super().__init__(window)
        self.fps_display = FPSDisplay(window=window, color=(255, 0, 0, 255))

        self.error_message = ""

        self.error_label = Label(
            self.error_message,
            x=300,
            y=10,
            color=(255, 0, 0, 255),
            font_size=15,
        )

    def on_error(self, error: Error) -> None:
        self.error_message = f"{ErrorType(error.type).name}: {error.message}"

    def draw(self) -> None:
        self.fps_display.draw()
        # self.error_label.draw()

    def update(self, dt: float) -> None:
        return
        self.error_label.text = self.error_message
