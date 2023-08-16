from typing import TYPE_CHECKING, Callable, cast

from pyglet.gl import GL_SCISSOR_TEST, glDisable, glEnable, glScissor
from pyglet.graphics import Batch, Group
from pyglet.gui import Frame
from pyglet.image import Animation, Texture
from pyglet.text import Label
from pyglet.window import Window

import client
from client.game.nearest_sprite import NearestSprite
from client.game.ui import get_ui_grid
from client.game.ui.button import ImageButton
from client.game.ui.slider import Slider
from client.game.ui.tilebox import TileBox
from client.game.ui.utils import Exit
from client.scenes.scenemanager import Scene
from shared.gen.messages.v1 import Item

if TYPE_CHECKING:
    from client.scenes.game import Game


class SmallItem(Group):
    icon: int
    name: str
    description: str
    quantity: int

    def __init__(
        self,
        x: int,
        y: int,
        icon: int,
        name: str,
        description: str,
        quantity: int,
        order: int = 0,
        batch: Batch | None = None,
        parent: Group | None = None,
    ) -> None:
        super().__init__(order, parent)

        self._x = x
        self._y = y
        self.icon = icon
        self.name = name
        self.description = description
        self.quantity = quantity

        self._image = NearestSprite(
            cast(Texture, get_ui_grid()[self.icon]),
            x=x + cast(int, get_ui_grid().item_width) * 3,
            y=y - (cast(int, get_ui_grid().item_height) // 2),
            origin=(
                cast(int, get_ui_grid().item_width) // 2,
                cast(int, get_ui_grid().item_height) // 2,
            ),
            group=self,
        )
        self._image.scale = 3

        self._name_label = Label(
            text=f"{self.quantity}x {self.name}",
            x=x + cast(int, get_ui_grid().item_width) * 3 + 50,
            y=y,
            batch=batch,
            group=self,
            anchor_y="center",
            color=(0, 0, 0, 255),
            font_size=20,
        )

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        self._x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        offset = self._y - y

        self._image.y -= offset

        if self._name_label:
            self._name_label.y -= offset

        self._y = y

    def draw(self) -> None:
        self._image.draw()

    def __del__(self) -> None:
        self._name_label.__del__()


class InventoryItem:
    item: Item

    width: int
    height: int

    _x: int
    _y: int

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        item: Item,
        batch: Batch,
        group: Group,
        frame: Frame,
        cb: Callable[[Item], None],
    ) -> None:
        self.item = item

        self._x = x
        self._y = y

        self.width = width
        self.height = height

        self.frame = frame

        self.cb = cb

        self._first_item = SmallItem(
            x=x,
            y=y + height // 2,
            icon=self.item.icon,
            name=self.item.name,
            description=self.item.description,
            quantity=self.item.quantity,
            batch=batch,
            parent=group,
        )

        self._outline = TileBox(
            x,
            y,
            width,
            height,
            tile_offset_x=3,
            tile_offset_y=15,
            group=group,
        )

        self._show_button = ImageButton(
            img=Animation.from_image_sequence(
                get_ui_grid()[61 * 7 + 54 : 61 * 7 + 57],
                duration=0.01,
            ),
            x=x + 300,
            y=y + height // 2 - cast(int, get_ui_grid().item_height) // 2,
            group=group,
            scale_x=3,
            scale_y=3,
        )

        self.frame.add_widget(self._show_button)
        self._show_button.set_handler("on_press", self.show)

    def __del__(self) -> None:
        try:
            self.frame.remove_widget(self._show_button)
        except KeyError:
            pass

        self._first_item.__del__()

    def show(self) -> None:
        self.cb(self.item)

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        self._x = x
        self._outline.x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        offset = self._y - y

        self._outline.y += offset

        if self._first_item:
            self._first_item.y += offset

        self.frame.remove_widget(widget=self._show_button)
        self._show_button.y += offset
        self.frame.add_widget(widget=self._show_button)

        self._y = y

    def draw(self) -> None:
        self._outline.draw()
        self._show_button.draw()

        if self._first_item:
            self._first_item.draw()


class ShowItem(Group):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        order: int = 0,
        batch: Batch | None = None,
        parent: Group | None = None,
    ) -> None:
        super().__init__(order, parent)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self._outline = TileBox(
            x,
            y,
            width,
            height,
            tile_offset_x=3,
            tile_offset_y=15,
        )

        self._image = NearestSprite(
            img=cast(Texture, get_ui_grid()[61 * 3 + 16]),
            x=x + width // 2 - (cast(int, get_ui_grid().item_width)) // 2,
            y=y + 275,
            origin=(
                cast(int, get_ui_grid().item_width) // 2,
                cast(int, get_ui_grid().item_height) // 2,
            ),
            group=self,
        )
        self._image.scale = 15

        self._description_label = Label(
            text="",
            x=x + cast(int, get_ui_grid().item_width) * 3,
            y=y + 150,
            width=width - +cast(int, get_ui_grid().item_width) * 7,
            multiline=True,
            batch=batch,
            group=self,
            color=(0, 0, 0, 255),
            font_size=10,
        )

    def draw(self) -> None:
        self._outline.draw()
        self._image.draw()

    def set_item(self, item: Item) -> None:
        self._image.image = cast(Texture, get_ui_grid()[item.icon])
        self._description_label.text = item.description

    def reset(self) -> None:
        self._image.image = cast(Texture, get_ui_grid()[61 * 3 + 16])
        self._description_label.text = ""


class InnerInventory(Group):
    items_ui: list[InventoryItem]

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        batch: Batch,
        frame: Frame,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.batch = batch
        self.frame = frame

        self.items_ui = []
        self.item_height = 128

        self._show_item = ShowItem(
            x=x + self.width // 2,
            y=y,
            height=self.height,
            width=self.width // 2,
            batch=batch,
        )

        super().__init__()

    def recreate(self, items: list[Item]) -> None:
        for item in self.items_ui:
            item.__del__()

        self.items_ui = []

        self._show_item.reset()

        for i, item in enumerate(items):
            s = InventoryItem(
                x=self.x,
                y=self.height + self.y - self.item_height * (i + 1),
                width=self.width // 2,
                height=self.item_height,
                item=item,
                batch=self.batch,
                group=self,
                frame=self.frame,
                cb=self._show_item.set_item,
            )

            self.items_ui.append(s)

    def draw(self) -> None:
        self._show_item.draw()

        for item in self.items_ui:
            item.draw()

    def set_state(self) -> None:
        glEnable(GL_SCISSOR_TEST)
        glScissor(self.x, self.y, self.width, self.height)

    def unset_state(self) -> None:
        glDisable(GL_SCISSOR_TEST)


class Inventory(Scene):
    def __init__(
        self,
        window: Window,
    ) -> None:
        super().__init__(window=window)

        x = 0
        y = 0
        width = window.width
        height = window.height

        self.items: list[Item] = []
        self._outline = TileBox(x, y, width, height)
        self.inner_width = (width // self._outline.tile_size) * self._outline.tile_size
        self.inner_height = (
            height // self._outline.tile_size
        ) * self._outline.tile_size
        self.batch = Batch()
        self.frame = Frame(window, order=4)
        self.uuid = ""

        self.slider = 0

        self._up_button = ImageButton(
            img=Animation.from_image_sequence(
                get_ui_grid()[61 * 13 + 54 : 61 * 13 + 57],
                duration=0.01,
            ),
            x=x + self.inner_width - cast(int, get_ui_grid().item_width) * 2 - 40,
            y=y + self.inner_height - cast(int, get_ui_grid().item_height) * 2 - 40,
            scale_x=3,
            scale_y=3,
        )
        self._up_button.set_handler("on_press", self._slide_up)

        self._down_button = ImageButton(
            img=Animation.from_image_sequence(
                get_ui_grid()[61 * 13 + 51 : 61 * 13 + 54],
                duration=0.01,
            ),
            x=x + self.inner_width - cast(int, get_ui_grid().item_width) * 2 - 40,
            y=y + 40 + cast(int, get_ui_grid().item_height),
            scale_x=3,
            scale_y=3,
        )
        self._down_button.set_handler("on_press", self._slide_down)

        self._slider = Slider(
            x=x + self.inner_width - cast(int, get_ui_grid().item_width) * 3 - 40,
            y=y + 40 + cast(int, get_ui_grid().item_height) * 3,
            batch=self.batch,
            width=cast(int, get_ui_grid().item_width) * 3,
            height=self.inner_height - cast(int, get_ui_grid().item_width) * 6 - 40 * 2,
        )
        self._slider.set_handler("on_change", self._slide)

        self.inner_shop = InnerInventory(
            x=x + self._outline.tile_size,
            y=y + self._outline.tile_size,
            width=(
                self.inner_width
                - 2 * self._outline.tile_size
                - cast(int, get_ui_grid().item_width) * 3
                - 25
            ),
            height=self.inner_height - 2 * self._outline.tile_size,
            batch=self.batch,
            frame=self.frame,
        )

        self._exit = Exit(
            x=-10,
            y=int(height - 32 * 2.75),
            exit_func=self._close,
            batch=self.batch,
            frame=self.frame,
        )

        self.dirty = True
        self.sider_step_size = self.inner_shop.item_height

        self._update_slider()

    def _close(self) -> None:
        cast("Game", client.scene_manager.current_scene).remove_inventory()

    def _max_slider(self) -> int:
        return (len(self.inner_shop.items_ui) - 1) * self.inner_shop.item_height

    def _slide(self, value: float) -> None:
        y = int((100 - value) / 100 * self._max_slider())
        step = self.slider - y

        self.slider = y
        self._update_item_y(step)

    def _update_slider(self) -> None:
        val = 100
        if self._max_slider() != 0:
            val = 100 - (self.slider / self._max_slider()) * 100

        self._slider.value = val

    def _slide_up(self) -> None:
        step = self.sider_step_size

        if self.slider - step < 0:
            step = self.slider % self.sider_step_size

            if step == self.sider_step_size:
                return

        self.slider -= step
        self._update_slider()
        self._update_item_y(step)

    def _slide_down(self) -> None:
        step = self.sider_step_size

        if self.slider + step > self._max_slider():
            step = self.sider_step_size - (self.slider % self.sider_step_size)

            if step == self.sider_step_size:
                return

        self.slider += step
        self._update_slider()
        self._update_item_y(-step)

    def _update_item_y(self, step: int) -> None:
        for item in self.inner_shop.items_ui:
            item.y += step

    def draw(self) -> None:
        if self.dirty:
            # TODO: Reuse old textures
            self.slider = 0
            self._update_slider()

            self.inner_shop.recreate(self.items)

            self.dirty = False

        self._outline.draw()

        self.inner_shop.draw()

        self.batch.draw()
        self._up_button.draw()
        self._down_button.draw()
        self._slider.draw()

        self._exit.draw()

    def set_inventory_items(self, items: list[Item]) -> None:
        self.items = items

        self.dirty = True

    def activate(self) -> None:
        self.frame.add_widget(widget=self._up_button)
        self.frame.add_widget(widget=self._down_button)
        self.frame.add_widget(widget=self._slider)

        self._exit.activate()

    def deactivate(self) -> None:
        self.reset()

        self.cb = None

        self.frame.remove_widget(widget=self._up_button)
        self.frame.remove_widget(widget=self._down_button)
        self.frame.remove_widget(widget=self._slider)

        self._exit.__del__()

    def reset(self) -> None:
        self.text = []
