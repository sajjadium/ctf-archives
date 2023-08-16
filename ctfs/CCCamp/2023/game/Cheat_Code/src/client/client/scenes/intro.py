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


class Intro(Scene):
    status: str

    def get_background_image(self) -> ImageData:
        return cast(
            ImageData,
            image.load(Path(client.PATH, "assets/intro_background.png")),
        )

    def __init__(self, window: Window) -> None:
        super().__init__(window)

        self.frame = Frame(window, order=4)
        self.batch = Batch()
        self.status = ""

        self.background_image = self.get_background_image()
        self.background = Sprite(img=self.background_image, x=0, y=0, batch=self.batch)

        self.press_key_label = Label(
            text="Press any key to continue ...",
            font_name="Consolas",
            font_size=14,
            x=600,
            y=100,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=500,
            batch=self.batch,
        )

        self.game_logo = Sprite(
            img=image.load_animation(Path(client.PATH, "assets/game_logo.gif")),
            x=100,
            y=280,
            batch=self.batch,
        )

    def activate(self) -> None:
        super().activate()

    def deactivate(self) -> None:
        super().deactivate()

    def draw(self) -> None:
        self.batch.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        client.scene_manager.set_scene(scene="mainmenu")

    def update(self, dt: float) -> None:
        pass
        # self.status_label.text = self.status
