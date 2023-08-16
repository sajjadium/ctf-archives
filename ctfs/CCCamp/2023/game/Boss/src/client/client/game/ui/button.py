from typing import cast

from pyglet.graphics import Batch, Group
from pyglet.gui.widgets import WidgetBase
from pyglet.image import Animation, AnimationFrame, Texture
from pyglet.text import Label

from client.game.nearest_sprite import NearestSprite
from client.game.ui.tilebox import TileStrip


class ButtonBase(WidgetBase):
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self._pressed = False
        self.enabled = True
        self._hover = False

        super().__init__(x, y, width, height)

    def pressed(self) -> None:
        pass

    def released(self) -> None:
        pass

    def on_mouse_press(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled or not self._check_hit(x, y):
            return
        self._pressed = True
        self.pressed()
        self.dispatch_event("on_press")

    def on_mouse_release(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled or not self._pressed:
            return
        self._pressed = False
        self.released()
        self.dispatch_event("on_release")

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        if not self.enabled or not self._check_hit(x, y):
            self._hover = False
            return
        self._hover = True

    def _update_position(self) -> None:
        pass


ButtonBase.register_event_type("on_press")
ButtonBase.register_event_type("on_release")


class Button(ButtonBase):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        batch: Batch,
        group: Group | None = None,
        color: tuple[int, int, int, int] = (80, 0, 80, 255),
    ) -> None:
        self._outline = TileStrip(
            x + 24,
            y,
            width + 16 * 3,
            height=height,
            tile_offset_x=3,
            tile_offset_y=23,
            scale_y=1.2,
            scale_x=1.2,
            group=group,
        )
        self._outline.x -= 32

        super().__init__(
            x + 8 * self._outline.scale_x,
            y - 8,
            (self._outline.width - 16 * 3) * self._outline.scale_x,
            (self._outline.height) * self._outline.scale_y,
        )

    def _update_position(self) -> None:
        self._outline.x = self._x
        self._outline.y = self._y

    def draw(self) -> None:
        if self._hover:
            self._outline.color_add = (0.1, 0.1, 0.1)
        else:
            self._outline.color_add = (0, 0, 0)
        self._outline.draw()


class TextButton(Button):
    def __init__(
        self, text: str, x: int, y: int, batch: Batch, group: Group | None = None
    ) -> None:
        self._label = Label(
            text,
            x=x,
            y=y + 4,
            batch=batch,
            group=group,
            anchor_y="bottom",
            color=(0, 0, 0, 255),
        )
        label_width = self._label.content_width
        label_height = cast(int, self._label.content_height)
        width = label_width
        height = label_height
        super().__init__(x, y, width, height, batch, group=group)
        self._label.x += label_width / 2 - 4

    def draw(self) -> None:
        super().draw()

    def _update_position(self) -> None:
        self._label.x = self._x
        self._label.y = self._y

        super()._update_position()


class ImageButton(ButtonBase):
    def __init__(
        self,
        img: Texture | Animation,
        x: int,
        y: int,
        group: Group | None = None,
        scale_x: float = 1.0,
        scale_y: float = 1.0,
    ) -> None:
        match img:
            case Texture() as t:
                width = t.width
                height = t.height
                self._animate = False
            case Animation():
                width = cast(int, img.get_max_width())
                height = cast(int, img.get_max_height())
                self._animate = True

                cast(AnimationFrame, img.frames[-1]).duration = None

        self._image = NearestSprite(
            img=img,
            x=x,
            y=y,
            group=group,
            origin=(width // 2, height // 2),
        )

        if self._animate:
            self._image.paused = True

        self._image.scale_x = scale_x
        self._image.scale_y = scale_y

        self._w = width
        self._h = height

        super().__init__(
            x - (self._w * (self._image.scale_x - 1)) / 2,
            y - (self._h * (self._image.scale_y - 1)) / 2,
            width * scale_x,
            height * scale_y,
        )

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._image.x = value + (self._w * (self._image.scale_x - 1)) / 2
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._image.y = value + (self._h * (self._image.scale_y - 1)) / 2
        self._y = value

    def pressed(self) -> None:
        if self._animate:
            self._image.paused = False

    def released(self) -> None:
        if self._animate:
            self._image._next_dt = 0  # pyright: ignore[reportPrivateUsage]
            self._image._animate(0)  # pyright: ignore[reportPrivateUsage]

            self._image.paused = True

    def draw(self) -> None:
        self._image.draw()
