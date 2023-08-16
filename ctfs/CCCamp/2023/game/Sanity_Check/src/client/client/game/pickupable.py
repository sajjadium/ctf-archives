from dataclasses import dataclass
from typing import Any, cast

from pyglet.image import Texture

from client.game.entities.entity import ServerManagedEntity
from client.game.nearest_sprite import NearestSprite
from client.game.ui import get_ui_grid
from shared.gen.messages.v1 import Item


@dataclass
class Pickupable(ServerManagedEntity):
    uuid: str

    def __init__(
        self, item: Item, x: float, y: float, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.item = item

        self.x = x
        self.y = -y

        self.is_ready = True
        self.shrinking_rotate = False

    def on_load(self) -> None:
        origin_rotation = (
            cast(int, get_ui_grid().item_width) // 2,
            cast(int, get_ui_grid().item_height) // 2,
        )

        if self.item.icon >= 2562 and self.item.icon <= 2571:
            origin_rotation = (
                cast(int, get_ui_grid().item_width) // 2,
                0,
            )

        self.sprite = NearestSprite(
            cast(Texture, get_ui_grid()[self.item.icon]),
            x=int(self.x + cast(int, get_ui_grid().item_width) // 2),
            y=int(self.y - cast(int, get_ui_grid().item_height) // 2),
            origin_scale=(
                cast(int, get_ui_grid().item_width) // 2,
                cast(int, get_ui_grid().item_height) // 2,
            ),
            origin_rotation=origin_rotation,
        )
        self.sprite.scale = 1.25
        self.sprite.rotation = 0

        return super().on_load()

    def update(self, dt: float) -> None:
        if self.is_loaded:
            update = 10 * dt
            if self.shrinking_rotate:
                update *= -1

            self.sprite.rotation += update

            if self.sprite.rotation < -5:
                self.shrinking_rotate = False
            if self.sprite.rotation > 5:
                self.shrinking_rotate = True

        return super().update(dt)

    def draw(self) -> None:
        if self.is_loaded:
            self.sprite.draw()

        return super().draw()
