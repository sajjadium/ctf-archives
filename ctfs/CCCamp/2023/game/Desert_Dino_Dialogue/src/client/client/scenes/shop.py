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
from shared.gen.messages.v1 import ShopInteract, ShopInteractType

if TYPE_CHECKING:
    from client.scenes.game import Game

ShopCallback = Callable[[], None] | None


class Coin(Group):
    coins: int

    def __init__(
        self,
        x: int,
        y: int,
        coins: int,
        order: int = 0,
        batch: Batch | None = None,
        parent: Group | None = None,
    ) -> None:
        super().__init__(order, parent)

        self._x = x
        self._y = y
        self.coins = coins

        self._coin = NearestSprite(
            cast(Texture, get_ui_grid()[61 * 23 + 13]),
            x=x + cast(int, get_ui_grid().item_width) * 2,
            y=y - cast(int, get_ui_grid().item_height) // 2,
            origin=(
                cast(int, get_ui_grid().item_width) // 2,
                cast(int, get_ui_grid().item_height) // 2,
            ),
            group=self,
        )
        self._coin.scale = 3

        self._price_label = Label(
            str(coins),
            x=x + 15,
            y=y,
            batch=batch,
            group=self,
            anchor_y="center",
            anchor_x="right",
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

        if self._coin:
            self._coin.y -= offset

        if self._price_label:
            self._price_label.y -= offset

        self._y = y

    def draw(self) -> None:
        if self._coin:
            self._coin.draw()

    def __del__(self) -> None:
        self._price_label.__del__()

        self._coin.__del__()


class Item(Group):
    icon: int
    name: str
    quantity: int

    def __init__(
        self,
        x: int,
        y: int,
        icon: int,
        name: str,
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


class ShopItem:
    item: ShopInteract

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
        item: ShopInteract,
        batch: Batch,
        group: Group,
        frame: Frame,
    ) -> None:
        self.item = item

        self._x = x
        self._y = y

        self.width = width
        self.height = height

        self.frame = frame

        self._first_item = Item(
            x=x,
            y=y + height // 2,
            icon=self.item.item.icon,
            name=self.item.item.name,
            quantity=self.item.item.quantity,
            batch=batch,
            parent=group,
        )

        if self.item.type == ShopInteractType.SHOP_INTERACT_TYPE_TRADE:
            self._second_item = Item(
                x=x + 300 + cast(int, get_ui_grid().item_width) * 3,
                y=y + height // 2,
                icon=self.item.trade_in.icon,
                name=self.item.trade_in.name,
                quantity=self.item.trade_in.quantity,
                batch=batch,
                parent=group,
            )
        else:
            self._second_item = Coin(
                x=x + 500 - 15,
                y=y + height // 2,
                coins=self.item.cost,
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

        self._buy_button = ImageButton(
            img=Animation.from_image_sequence(
                get_ui_grid()[61 * 17 + 54 : 61 * 17 + 57],
                duration=0.01,
            ),
            x=x + 700,
            y=y + height // 2 - cast(int, get_ui_grid().item_height) // 2,
            group=group,
            scale_x=3,
            scale_y=3,
        )

        arrow_index = 61 * 19 + 28
        if self.item.type == ShopInteractType.SHOP_INTERACT_TYPE_SELL:
            arrow_index = 61 * 19 + 29

        self._arrow_icon = NearestSprite(
            cast(Texture, get_ui_grid()[arrow_index]),
            x=x + 325,
            y=y + height // 2 - cast(int, get_ui_grid().item_height) // 2,
            origin=(
                cast(int, get_ui_grid().item_width) // 2,
                cast(int, get_ui_grid().item_height) // 2,
            ),
            group=group,
        )
        self._arrow_icon.scale = 3

        self.frame.add_widget(self._buy_button)
        self._buy_button.set_handler("on_press", self.buy)

    def __del__(self) -> None:
        try:
            self.frame.remove_widget(self._buy_button)
        except KeyError:
            pass

        self._second_item.__del__()

        self._first_item.__del__()

    def buy(self) -> None:
        cast("Game", client.scene_manager.current_scene).buy(self.item)

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

        if self._second_item:
            self._second_item.y += offset

        if self._first_item:
            self._first_item.y += offset

        self._arrow_icon.y += offset

        self.frame.remove_widget(widget=self._buy_button)
        self._buy_button.y += offset
        self.frame.add_widget(widget=self._buy_button)

        self._y = y

    def draw(self) -> None:
        self._outline.draw()
        self._buy_button.draw()
        self._arrow_icon.draw()

        self._second_item.draw()

        self._first_item.draw()


class InnerShop(Group):
    shop_items_ui: list[ShopItem]

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

        self.shop_items_ui = []
        self.item_height = 128

        super().__init__()

    def recreate(self, items: list[ShopInteract]) -> None:
        for item in self.shop_items_ui:
            item.__del__()
            del item
            item = None

        self.shop_items_ui = []

        for i, item in enumerate(items):
            s = ShopItem(
                x=self.x,
                y=self.height + self.y - self.item_height * (i + 1),
                width=self.width,
                height=self.item_height,
                item=item,
                batch=self.batch,
                group=self,
                frame=self.frame,
            )

            self.shop_items_ui.append(s)

    def draw(self) -> None:
        for item in self.shop_items_ui:
            item.draw()

    def set_state(self) -> None:
        glEnable(GL_SCISSOR_TEST)
        glScissor(self.x, self.y, self.width, self.height)

    def unset_state(self) -> None:
        glDisable(GL_SCISSOR_TEST)


class Shop(Scene):
    def __init__(
        self,
        window: Window,
        cb: ShopCallback = None,
    ) -> None:
        super().__init__(window=window)

        x = 0
        y = 0
        width = window.width
        height = window.height

        self.items: list[ShopInteract] = []
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

        self.cb = cb

        self.inner_shop = InnerShop(
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
        cast("Game", client.scene_manager.current_scene).remove_shop()

    def _max_slider(self) -> int:
        return (len(self.inner_shop.shop_items_ui) - 1) * self.inner_shop.item_height

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
        for item in self.inner_shop.shop_items_ui:
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

    def set_shop_items(self, items: list[ShopInteract], uuid: str) -> None:
        self.items = items
        self.uuid = uuid

        self.dirty = True

    def start(
        self, items: list[ShopInteract], uuid: str, cb: ShopCallback = None
    ) -> None:
        self.items = items
        self.cb = cb
        self.uuid = uuid

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
        self.uuid = ""
