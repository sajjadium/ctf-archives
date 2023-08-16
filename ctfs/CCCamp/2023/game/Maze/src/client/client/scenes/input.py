from typing import TYPE_CHECKING, Callable, cast

from pyglet.graphics import Batch
from pyglet.window import Window
from pyglet.window.key import ENTER

import client
from client.game.ui.input import TextInput
from client.scenes.scenemanager import Scene

if TYPE_CHECKING:
    from client.scenes.game import Game

InputCallback = Callable[[str], None] | None


class InputScene(Scene):
    callback: InputCallback

    def __init__(
        self,
        window: Window,
    ) -> None:
        super().__init__(window=window)

        self.batch = Batch()

        self.input = TextInput(
            "",
            32,
            32,
            self.window.width - 32 * 2,
            batch=self.batch,
            text_color=(0, 0, 0, 255),
            caret_color=(0, 0, 0, 255),
            color=(0, 0, 0, 0),
        )

    def on_key_press(self, symbol: int, modifiers: int) -> int | None:
        if symbol == ENTER:
            if self.callback:
                self.callback(self.input.value)

            self.input.value = ""

            game = cast("Game", client.scene_manager.current_scene)
            game.remove_input()

        return super().on_key_press(symbol, modifiers)

    def draw(self) -> None:
        self.input.draw()
        self.batch.draw()

        return super().draw()

    def activate(self) -> None:
        self.window.push_handlers(self.input)

    def deactivate(self) -> None:
        self.cb = None
        self.window.remove_handlers(self.input)
