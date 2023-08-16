from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Dict, Tuple, cast

from pyglet import shapes
from pyglet.graphics import Batch
from pyglet.image import Animation, AnimationFrame, ImageData, ImageGrid, TextureGrid
from pyglet.math import Mat4, Vec3
from pyglet.sprite import Sprite
from pyglet.text import Label

import client
from client.game.entities.renderable import Renderable
from client.game.nearest_sprite import NearestSprite
from shared.constants import NUM_TILES_PER_COLUM
from shared.gen.messages.v1 import Activity
from shared.gen.messages.v1 import Direction as DirectionProto
from shared.gen.messages.v1 import EntityAssets

if TYPE_CHECKING:
    from client.scenes.game import Game


DEBUG_INTERACTION = False


class Direction(IntEnum):
    UP = 0
    RIGHT = 90
    LEFT = 270
    DOWN = 180


@dataclass
class Entity(Renderable):
    x: float
    y: float
    width: float
    height: float
    rotation: float

    def __init__(self, *args: int, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)

        self.x = 0.0
        self.y = 0.0
        self.width = 0.0
        self.height = 0.0

    def on_load(self) -> None:
        super().on_load()


@dataclass
class SpriteEntity(Entity):
    sprite: Sprite | None

    def __init__(self, *args: int, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)

        self.sprite = None

    def on_load(self) -> None:
        super().on_load()

    def draw(self) -> None:
        super().draw()

        if self.sprite is not None:
            self.sprite.x = self.x
            self.sprite.y = -self.y  # convert between tiled and pyglet coords
            self.sprite.draw()


@dataclass
class TilesetEntity(SpriteEntity):
    assets: EntityAssets
    sprites: Dict[Activity, Dict[DirectionProto, Sprite]]
    activity: Activity

    def __init__(self, *args: int, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)

        self.activity = Activity.ACTIVITY_IDLE
        self.sprites = defaultdict(lambda: {})

    def set_assets(self, assets: EntityAssets) -> None:
        self.assets = assets
        self.is_ready = True

    def on_load(self) -> None:
        self.width = self.assets.width
        self.height = self.assets.height

        tileset = self.assets.tileset

        sprite_image = ImageData(
            tileset.width, tileset.height, "RGBA", tileset.tileset, tileset.width * -4
        )

        rows = tileset.height // self.height

        image_grid = ImageGrid(
            sprite_image,
            rows=rows,
            columns=NUM_TILES_PER_COLUM,
        )

        texture_grid: TextureGrid = image_grid.get_texture_sequence()

        for asset in self.assets.entity_assets:
            animation = next((a for a in tileset.animations if a.id == asset.id), None)

            if animation is None:
                sprite = NearestSprite(
                    Animation.from_image_sequence(  # type: ignore
                        texture_grid[
                            (
                                rows - 1 - (asset.id // NUM_TILES_PER_COLUM),
                                asset.id % NUM_TILES_PER_COLUM,
                            ) : (
                                rows - 1 - (asset.id // NUM_TILES_PER_COLUM) + 1,
                                (asset.id % NUM_TILES_PER_COLUM) + 1,
                            )
                        ],
                        duration=0.1,
                    ),
                    origin=(self.width / 2, self.height / 2),
                )
            else:
                frames = [
                    AnimationFrame(
                        image=texture_grid[  # type: ignore
                            (
                                rows - 1 - (step.id // NUM_TILES_PER_COLUM),
                                step.id % NUM_TILES_PER_COLUM,
                            ) : (
                                rows - 1 - (step.id // NUM_TILES_PER_COLUM) + 1,
                                (step.id % NUM_TILES_PER_COLUM) + 1,
                            )
                        ][0],
                        duration=step.duration / 1000,
                    )
                    for step in animation.animation_setps
                ]

                sprite = NearestSprite(
                    Animation(frames=frames), origin=(self.width / 2, self.height / 2)
                )

            self.sprites[asset.activity][asset.direction] = sprite

        self.activity, direction_sprite = list(self.sprites.items())[0]
        self.direction = list(direction_sprite.keys())[0]

        super().on_load()

    def rotation_to_directionproto(self):
        match (int(self.rotation // 90) % 4) * 90:
            case Direction.UP.value:
                d = DirectionProto.DIRECTION_NORTH
            case Direction.RIGHT.value:
                d = DirectionProto.DIRECTION_EAST
            case Direction.DOWN.value:
                d = DirectionProto.DIRECTION_SOUTH
            case Direction.LEFT.value:
                d = DirectionProto.DIRECTION_WEST
            case _:
                assert False, "This should never be reached"
        return d

    def update(self, dt: float) -> None:
        if self.is_loaded:
            d = self.rotation_to_directionproto()

            self.sprite = self.sprites[self.activity][d]

        super().update(dt)


@dataclass
class InteractEntity(Entity):
    interact_distance: float
    interact_offset: Tuple[float, float]
    interactable: bool

    if DEBUG_INTERACTION:
        interaction_bb: shapes.Circle | None

    def __init__(
        self,
        interact_offset: Tuple[float, float] = (0, 0),
        interact_distance: float = 0,
        *args: int,
        **kwargs: str,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.interact_offset = interact_offset
        self.interact_distance = interact_distance
        if DEBUG_INTERACTION:
            self.interaction_bb = None
        self.interactable = True

    def on_load(self) -> None:
        super().on_load()

        self.interact_offset = (self.width / 2, -self.height / 2)

        if DEBUG_INTERACTION:
            self.interaction_bb = shapes.Circle(
                self.x + self.interact_offset[0],
                -(self.y + self.interact_offset[1]),
                self.interact_distance,
                color=(80, 80, 0, 230),
            )

    def draw(self) -> None:
        super().draw()
        if DEBUG_INTERACTION:
            if self.interaction_bb:
                self.interaction_bb.x = self.x + self.interact_offset[0]
                self.interaction_bb.y = -(self.y + self.interact_offset[1])
                self.interaction_bb.draw()

    def stop_interaction(self) -> None:
        self.in_interaction = False

    def interact(self) -> None:
        self.in_interaction = True


@dataclass
class NamedEntity(Entity):
    label: str
    username_label: Label | None
    batch: Batch | None

    def __init__(self, batch: Batch | None = None, *args: int, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)

        self.label = ""
        self.username_label = None
        self.batch = batch

    def on_load(self) -> None:
        self.username_label = Label(
            self.label,
            x=0,
            y=0,
            color=(0, 0, 0, 255),
            anchor_x="center",
            font_name="Times New Roman",
            font_size=12,
            batch=self.batch,
        )

        super().on_load()

    def update(self, dt: float) -> None:
        if self.username_label:
            if self.label != self.username_label.text:
                self.username_label.text = self.label

            self.username_label.x = self.x + self.width / 2
            self.username_label.y = -self.y + 40

        super().update(dt)

    def draw(self) -> None:
        if self.username_label is not None:
            # This is hack AF, pyglet should fix their label shaders
            window = client.scene_manager.window
            game = cast("Game", client.scene_manager.current_scene)
            zoom: float = game.camera.zoom

            old_window_view = window.view
            window.view = (
                window.view
                @ Mat4.from_translation(
                    Vec3(
                        cast(int, self.username_label.x),
                        cast(int, self.username_label.y),
                        0,
                    )
                )
                @ Mat4.from_scale(Vec3(1 / zoom, 1 / zoom, 1))
                @ Mat4.from_translation(
                    Vec3(
                        -cast(int, self.username_label.x),
                        -cast(int, self.username_label.y),
                        0,
                    )
                )
            )
            # self.username_label.font_size = 12 * zoom
            if self.batch is None:
                self.username_label.draw()

            window.view = old_window_view

        return super().draw()


@dataclass
class ServerManagedEntity(Entity):
    uuid: str

    def __init__(self, uuid: str, *args: int, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)

        self.uuid = uuid

    def on_load(self) -> None:
        super().on_load()

    def update(self, dt: float) -> None:
        super().update(dt)

    def draw(self) -> None:
        return super().draw()
