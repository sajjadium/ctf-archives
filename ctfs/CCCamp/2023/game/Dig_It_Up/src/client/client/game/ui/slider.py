from typing import cast

from pyglet.graphics import Batch, Group
from pyglet.gui.widgets import WidgetBase
from pyglet.image import Texture

from client.game.nearest_sprite import NearestSprite
from client.game.ui import get_ui_grid
from client.game.ui.tilebox import TileStrip


class Slider(WidgetBase):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        batch: Batch | None = None,
        group: Group | None = None,
    ) -> None:
        edge = 0
        knob_height = 64
        knob_width = width + 32

        super().__init__(x, y, max(width, knob_width), height)
        self._edge = edge
        self._half_knob_width = knob_width / 2
        self._half_knob_height = knob_height / 2

        self._min_knob_y = y + edge
        self._max_knob_y = y + height - knob_height - edge

        self._user_group = group
        bg_group = Group(order=0, parent=group)
        fg_group = Group(order=1, parent=group)

        new_height = ((height / 2) // 32) * 32
        self._base_spr = TileStrip(
            x - width % 32 - 4,
            y + height / 2 - new_height / 2,
            group=bg_group,
            width=int(width),
            height=int(new_height),
            horizontal=False,
            tile_offset_x=19,
            tile_offset_y=6,
            scale_x=3.65,
            scale_y=3.65,
        )

        self._knob_spr = NearestSprite(
            cast(Texture, get_ui_grid()[61 * 5 + 22]),
            int(x + width / 2 - self._half_knob_width) - 2,
            int(y + edge),
            group=fg_group,
        )
        self._knob_spr.scale_x = knob_width / 16
        self._knob_spr.scale_y = knob_height / 16

        self._value = 0
        self._in_update = False

    def draw(self) -> None:
        self._base_spr.draw()
        self._knob_spr.draw()

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value
        y = (
            (self._max_knob_y - self._min_knob_y) * value / 100
            + self._min_knob_y
            + self._half_knob_height
        )
        self._knob_spr.y = max(
            self._min_knob_y, min(y - self._half_knob_height, self._max_knob_y)
        )

    @property
    def _min_x(self) -> float:
        return cast(float, self._x - self._half_knob_width)

    @property
    def _max_x(self) -> float:
        return cast(float, self._x + self._half_knob_width + self.width / 2)

    @property
    def _min_y(self) -> float:
        return cast(float, self._y + self._edge)

    @property
    def _max_y(self) -> float:
        return cast(float, self._y + self._height - self._edge)

    def _check_hit(self, x: int, y: int) -> bool:
        return self._min_x < x < self._max_x and self._min_y < y < self._max_y

    def _update_knob(self, y: float) -> None:
        self._knob_spr.y = max(
            self._min_knob_y, min(y - self._half_knob_height, self._max_knob_y)
        )
        self._value = abs(
            ((self._knob_spr.y - self._min_knob_y) * 100)
            / (self._min_knob_y - self._max_knob_y)
        )
        self.dispatch_event("on_change", self._value)

    def on_mouse_press(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled:
            return

        if self._check_hit(x, y):
            self._in_update = True
            self._update_knob(y)

    def on_mouse_drag(
        self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int
    ) -> None:
        if not self.enabled:
            return

        if self._in_update:
            self._update_knob(y)

    def on_mouse_scroll(self, x: int, y: int, mouse: int, direction: int) -> None:
        if not self.enabled:
            return

        if self._check_hit(x, y):
            self._update_knob(self._knob_spr.y + self._half_knob_height + direction)

    def on_mouse_release(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled:
            return
        self._in_update = False


Slider.register_event_type("on_change")
