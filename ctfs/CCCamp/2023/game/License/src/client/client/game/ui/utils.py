from typing import Callable, cast

from pyglet.graphics import Batch, Group
from pyglet.gui import Frame
from pyglet.image import Animation

from client.game.ui import get_ui_grid
from client.game.ui.button import ImageButton
from client.game.ui.tilebox import TileBox


class Exit(Group):
    height: int = 32 * 3

    def __init__(
        self,
        x: int,
        y: int,
        exit_func: Callable[[], None],
        frame: Frame,
        batch: Batch | None = None,
        order: int = 0,
        parent: Group | None = None,
    ) -> None:
        super().__init__(order, parent)
        self.frame = frame
        self.exit_func = exit_func

        self.exit_button = ImageButton(
            img=Animation.from_image_sequence(
                get_ui_grid()[61 * 3 + 48 : 61 * 3 + 51],
                duration=0.01,
            ),
            x=x + self.height // 2 - cast(int, get_ui_grid().item_width) // 2,
            y=y + self.height // 2 - cast(int, get_ui_grid().item_height) // 2,
            scale_x=2,
            scale_y=2,
            group=self,
        )
        self.exit_button.set_handler("on_press", self.exit)

        self.bg = TileBox(
            x=x,
            y=y,
            width=self.height,
            height=self.height,
            tile_size=32,
            tile_offset_x=3,
            tile_offset_y=10,
            group=self,
        )

    def activate(self) -> None:
        self.frame.add_widget(self.exit_button)

    def exit(self) -> None:
        self.exit_func()

    def draw(self) -> None:
        if self.bg:
            self.bg.draw()
        if self.exit_button:
            self.exit_button.draw()

    def __del__(self) -> None:
        self.frame.remove_widget(self.exit_button)
