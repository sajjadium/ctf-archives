from pathlib import Path
from typing import cast

from pyglet import image
from pyglet.graphics import Batch
from pyglet.gui import Frame
from pyglet.image import ImageData
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import Window

import client
from client.scenes.scenemanager import Scene
from shared.constants import PLAYER_DEATH_TIMEOUT


class GameOver(Scene):
    status: str

    def get_background_image(self) -> ImageData:
        return cast(
            ImageData,
            image.load(Path(client.PATH, "assets/game_over_background.png")),
        )

    def __init__(self, window: Window) -> None:
        super().__init__(window)

        self.frame = Frame(window, order=4)
        self.batch = Batch()
        self.status = ""

        self.background_image = self.get_background_image()
        self.background = Sprite(
            img=self.background_image, x=200, y=280, batch=self.batch
        )

        self.press_key_label = Label(
            text=f"You have to wait for {int(PLAYER_DEATH_TIMEOUT / 60)} minutes before you can respawn",
            font_name="Consolas",
            font_size=14,
            x=550,
            y=100,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=700,
            batch=self.batch,
        )

    def activate(self) -> None:
        super().activate()

    def deactivate(self) -> None:
        super().deactivate()

    def draw(self) -> None:
        self.batch.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        pass

    def update(self, dt: float) -> None:
        pass
        # self.status_label.text = self.status
