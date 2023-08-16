from typing import TYPE_CHECKING, cast

from pyglet.graphics import Batch, Group
from pyglet.gui import Frame
from pyglet.image import Animation, Texture
from pyglet.text import Label
from pyglet.window import Window

import client
from client.game.nearest_sprite import NearestSprite
from client.game.ui import get_ui_grid
from client.game.ui.button import ImageButton
from client.game.ui.tilebox import TileBox
from client.scenes.scenemanager import Scene
from shared.gen.messages.v1 import User

if TYPE_CHECKING:
    from client.scenes.game import Game


class Inventory(Group):
    height: int = 32 * 3

    def __init__(
        self,
        batch: Batch | None = None,
        frame: Frame | None = None,
        order: int = 0,
        parent: Group | None = None,
    ) -> None:
        super().__init__(order, parent)
        self.inventory_button = ImageButton(
            img=Animation.from_image_sequence(
                get_ui_grid()[61 * 1 + 51 : 61 * 1 + 54],
                duration=0.01,
            ),
            x=-1,
            y=0,
            scale_x=2,
            scale_y=2,
            group=self,
        )
        self.inventory_button.set_handler("on_press", self._on_press)

        self.bg = TileBox(
            x=0,
            y=0,
            width=0,
            height=self.height,
            tile_size=32,
            tile_offset_x=3,
            tile_offset_y=10,
            group=self,
        )
        self.frame = frame

    def deactivate(self) -> None:
        if self.frame:
            self.frame.remove_widget(self.inventory_button)

    def _on_press(self) -> None:
        cast("Game", client.scene_manager.current_scene).display_inventory()

    def on_resize(self, parent_height: int, window: Window) -> None:
        if self.inventory_button and self.bg:
            if self.frame and self.inventory_button._image.x != -1:
                self.frame.remove_widget(self.inventory_button)
            self.inventory_button.x = window.width - self.inventory_button.width * 2
            self.inventory_button.y = (
                parent_height / 2 - self.inventory_button.height / 2
            )
            if self.frame:
                self.frame.add_widget(self.inventory_button)
            self.bg.x = self.inventory_button.x - (32)
            self.bg.y = 0
            self.bg.width = 32 * 3

    def draw(self) -> None:
        if self.bg:
            self.bg.draw()
        if self.inventory_button:
            self.inventory_button.draw()

    def __del__(self) -> None:
        if self.frame:
            self.frame.remove_widget(self.inventory_button)
        del self.inventory_button
        self.inventory_button = None


class Logout(Group):
    height: int = 32 * 3

    def __init__(
        self,
        batch: Batch | None = None,
        frame: Frame | None = None,
        order: int = 0,
        parent: Group | None = None,
    ) -> None:
        super().__init__(order, parent)
        self.logout_button = ImageButton(
            img=Animation.from_image_sequence(
                get_ui_grid()[61 * 3 + 48 : 61 * 3 + 51],
                duration=0.01,
            ),
            x=-1,
            y=0,
            scale_x=2,
            scale_y=2,
            group=self,
        )
        self.logout_button.set_handler("on_press", self._on_press)

        self.bg = TileBox(
            x=0,
            y=0,
            width=0,
            height=self.height,
            tile_size=32,
            tile_offset_x=3,
            tile_offset_y=10,
            group=self,
        )
        self.frame = frame

    def _on_press(self) -> None:
        cast("Game", client.scene_manager.current_scene).logout()

    def on_resize(self, parent_height: int, window: Window):
        if self.logout_button and self.bg:
            if self.frame and self.logout_button._image.x != -1:
                self.frame.remove_widget(self.logout_button)
            self.logout_button.x = window.width - self.logout_button.width * 2
            self.logout_button.y = window.height - parent_height / 2
            if self.frame:
                self.frame.add_widget(self.logout_button)
            self.bg.x = self.logout_button.x - (32)
            self.bg.y = self.logout_button.y - (32)
            self.bg.width = 32 * 3

    def draw(self) -> None:
        if self.bg:
            self.bg.draw()
        if self.logout_button:
            self.logout_button.draw()

    def __del__(self) -> None:
        del self.logout_button
        self.logout_button = None

    def deactivate(self) -> None:
        if self.frame:
            self.frame.remove_widget(self.logout_button)


class Coins(Group):
    coins: int = 1337
    height: int = 32 * 3

    def __init__(
        self, batch: Batch | None = None, order: int = 0, parent: Group | None = None
    ) -> None:
        super().__init__(order, parent)
        self.label = Label(
            "",
            x=0,
            y=0,
            batch=batch,
            group=self,
            anchor_y="center",
            anchor_x="right",
            font_size=16,
            color=(80, 0, 0, 255),
        )
        self.bg = TileBox(
            x=0,
            y=0,
            width=0,
            height=self.height,
            tile_size=32,
            tile_offset_x=3,
            tile_offset_y=10,
            group=self,
        )
        self.coin = NearestSprite(
            cast(Texture, get_ui_grid()[61 * 23 + 13]),
            x=0,
            y=0,
            origin=(
                cast(int, get_ui_grid().item_width) / 2,
                cast(int, get_ui_grid().item_height) / 2,
            ),
            group=self,
        )
        self.coin.scale = 2

    def update(self, dt: float) -> None:
        match client.game_state.my_user:
            case User() as u:
                if self.label:
                    self.label.text = str(u.money)
            case _:
                pass

    def on_resize(self, parent_height: int, window: Window):
        if self.label:
            self.label.text = f"{self.coins}"
            width = (
                self.label.content_width + (-self.label.content_width) % 32
            ) + 32 * 3
            self.label.y = window.height - parent_height // 2
            self.label.x = width - 32 - 4
            if self.bg:
                self.bg.y = window.height - self.height
                self.bg.width = width
            if self.coin:
                self.coin.x = 32 + cast(int, get_ui_grid().item_width) / 2
                self.coin.y = (
                    window.height
                    - self.height // 2
                    - cast(int, get_ui_grid().item_height) / 2
                )

    def draw(self):
        if self.bg:
            self.bg.draw()
        if self.coin:
            self.coin.draw()

    def __del__(self):
        del self.bg
        self.bg = None
        del self.coin
        self.coin = None
        del self.label
        self.label = None


class Health(Group):
    health: int = 1337
    height: int = 32 * 3

    def __init__(
        self, batch: Batch | None = None, order: int = 0, parent: Group | None = None
    ) -> None:
        super().__init__(order, parent)
        self.label = Label(
            "",
            x=0,
            y=0,
            batch=batch,
            group=self,
            anchor_y="center",
            anchor_x="right",
            font_size=16,
            color=(80, 0, 0, 255),
        )
        self.bg = TileBox(
            x=0,
            y=0,
            width=0,
            height=self.height,
            tile_size=32,
            tile_offset_x=3,
            tile_offset_y=10,
            group=self,
        )
        self.heart = NearestSprite(
            img=cast(Texture, get_ui_grid()[61 * 10 + 11]),
            x=0,
            y=0,
            origin=(
                cast(int, get_ui_grid().item_width) / 2,
                cast(int, get_ui_grid().item_height) / 2,
            ),
            group=self,
        )
        self.heart.scale = 2

    def update(self, dt: float) -> None:
        match client.game_state.my_user:
            case User() as u:
                if self.label:
                    self.label.text = str(u.health)
            case _:
                pass

    def on_resize(self, parent_height: int, window: Window):
        if self.label:
            self.label.text = f"{self.health}"
            width = (
                self.label.content_width + (-self.label.content_width) % 32
            ) + 32 * 3
            self.label.y = window.height - parent_height // 2 - 64
            self.label.x = width - 32 - 4
            if self.bg:
                self.bg.y = window.height - self.height - 64
                self.bg.width = width
            if self.heart:
                self.heart.x = 32 + cast(int, get_ui_grid().item_width) / 2
                self.heart.y = (
                    window.height
                    - self.height // 2
                    - cast(int, get_ui_grid().item_height) / 2
                    - 64
                )

    def draw(self):
        if self.bg:
            self.bg.draw()
        if self.heart:
            self.heart.draw()

    def __del__(self):
        del self.bg
        self.bg = None
        del self.heart
        self.heart = None
        del self.label
        self.label = None


class UsernameLabel(Group):
    height: int = 32 * 3
    name: str = ""

    def __init__(
        self, batch: Batch | None = None, order: int = 0, parent: Group | None = None
    ) -> None:
        match client.game_state.my_user:
            case User() as u:
                self.name = u.username
            case _:
                pass

        super().__init__(order, parent)
        self.label = Label(
            "",
            x=0,
            y=0,
            batch=batch,
            group=self,
            anchor_y="center",
            anchor_x="center",
            font_size=16,
            color=(80, 0, 0, 255),
        )
        self.bg = TileBox(
            x=0,
            y=0,
            width=0,
            height=self.height,
            tile_size=32,
            tile_offset_x=3,
            tile_offset_y=10,
            group=self,
        )

    def on_resize(self, parent_height: int, window: Window):
        if self.label and self.bg:
            self.label.text = self.name
            self.label.x = window.width // 2
            self.label.y = window.height - parent_height // 2
            width = (
                self.label.content_width + (-self.label.content_width) % 32
            ) + 32 * 3
            self.bg.x = window.width // 2 - width // 2
            self.bg.y = window.height - self.height
            self.bg.width = width

    def draw(self):
        if self.bg:
            self.bg.draw()

    def __del__(self):
        del self.label
        self.label = None
        del self.bg
        self.bg = None


class HudTop(Group):
    height: int = 32 * 3

    def __init__(
        self,
        batch: Batch | None = None,
        frame: Frame | None = None,
        order: int = 0,
        parent: Group | None = None,
    ) -> None:
        super().__init__(order, parent)
        self.username = UsernameLabel(batch)
        self.coins = Coins(batch)
        self.health = Health(batch=batch)
        self.logout = Logout(batch, frame)

    def on_resize(self, window: Window):
        if self.username:
            self.username.on_resize(self.height, window)
        if self.coins:
            self.coins.on_resize(self.height, window)
        if self.health:
            self.health.on_resize(self.height, window)
        if self.logout:
            self.logout.on_resize(self.height, window)

    def update(self, dt: float) -> None:
        if self.coins:
            self.coins.update(dt)
        if self.health:
            self.health.update(dt)

    def draw(self):
        if self.username:
            self.username.draw()
        if self.coins:
            self.coins.draw()
        if self.health:
            self.health.draw()
        if self.logout:
            self.logout.draw()

    def __del__(self):
        del self.username
        self.username = None
        del self.coins
        self.coins = None
        del self.logout
        self.logout = None
        del self.health
        self.health = None

    def deactivate(self) -> None:
        if self.logout:
            self.logout.deactivate()


class HudBottom(Group):
    height: int = 32 * 3

    def __init__(
        self,
        batch: Batch | None = None,
        frame: Frame | None = None,
        order: int = 0,
        parent: Group | None = None,
    ) -> None:
        super().__init__(order, parent)
        self.inventory = Inventory(batch=batch, frame=frame, parent=self)

    def on_resize(self, window: Window):
        if self.inventory:
            self.inventory.on_resize(self.height, window)

    def update(self, dt: float) -> None:
        pass

    def draw(self):
        if self.inventory:
            self.inventory.draw()

    def __del__(self):
        del self.inventory
        self.inventory = None

    def deactivate(self) -> None:
        if self.inventory:
            self.inventory.deactivate()


class Hud(Scene):
    top: HudTop | None
    bottom: HudBottom | None

    def __init__(self, window: Window) -> None:
        super().__init__(window)
        self.frame = Frame(window, order=4)
        self.top = None
        self.bottom = None
        self.batch = None
        self.window = window

    def activate(self) -> None:
        self.batch = Batch()
        self.top = HudTop(self.batch, self.frame)
        self.top.on_resize(self.window)

        self.bottom = HudBottom(self.batch, self.frame)
        self.bottom.on_resize(self.window)

    def draw(self) -> None:
        if self.top:
            self.top.draw()

        if self.bottom:
            self.bottom.draw()

        if self.batch:
            self.batch.draw()

    def deactivate(self) -> None:
        if self.top:
            self.top.deactivate()
        del self.top
        self.top = None

        if self.bottom:
            self.bottom.deactivate()
        del self.bottom
        self.bottom = None

        del self.batch
        self.batch = None

        return super().deactivate()

    def update(self, dt: float) -> None:
        if self.top:
            self.top.update(dt)

        if self.bottom:
            self.bottom.update(dt)
