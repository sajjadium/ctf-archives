import random
from collections import defaultdict
from functools import cache
from pathlib import Path
from typing import cast

import pyglet
from pyglet.graphics import Batch
from pyglet.gui import Frame
from pyglet.image import ImageData
from pyglet.text import Label
from pyglet.window import Window
from pyglet.window.key import SPACE

import client
from client.game.nearest_sprite import NearestSprite
from client.scenes.scenemanager import Scene
from shared.gen.messages.v1 import Interact, InteractStatus
from shared.gen.messages.v1 import Runner as Runner
from shared.gen.messages.v1 import RunnerAction, RunnerEvent


@cache
def get_dino_image() -> ImageData:
    return cast(
        ImageData,
        pyglet.image.load(Path(client.PATH, "assets/google/100-offline-sprite.png")),
    )


class Background:
    def activate(self, batch: Batch) -> None:
        self.background_image = get_dino_image().get_region(2, 100 - 54 - 12, 1200, 12)
        self.background = pyglet.sprite.Sprite(
            self.background_image, 0, 200, batch=batch
        )
        self.background2 = pyglet.sprite.Sprite(
            self.background_image, self.background_image.width, 200, batch=batch
        )

    def update(self, dt: float, offset: float):
        self.background2.x = offset % self.background.width
        self.background.x = self.background2.x - self.background2.width


class Obstacle:
    sprite: NearestSprite
    x: float = 0
    width: float
    height: float

    def activate(self, batch: Batch) -> None:
        pass

    def update(self, dt: float, speed: float):
        pass

    def draw(self):
        pass


class LongObstacle(Obstacle):
    width = 75
    height = 50 - 2

    def activate(self, batch: Batch) -> None:
        self.sprite = NearestSprite(
            cast(
                pyglet.image.Texture,
                get_dino_image().get_region(407, 100 - 2 - 50, 75, height=50),
            ),
            -75,
            200 - 2,
        )

    def update(self, dt: float, speed: float):
        self.x -= dt * speed
        self.sprite.x = self.x

    def draw(self):
        self.sprite.draw()


class BigObstacle(Obstacle):
    width = 25
    height = 50 - 2

    def activate(self, batch: Batch) -> None:
        self.image = pyglet.image.ImageGrid(
            get_dino_image().get_region(332, 100 - 2 - 50, 25 * 3, height=50), 1, 3
        ).get_texture_sequence()

        self.sprite = NearestSprite(
            cast(pyglet.image.Texture, random.choice(self.image)),
            -self.image.item_width,
            200 - 2,
        )

    def update(self, dt: float, speed: float):
        self.x -= dt * speed
        self.sprite.x = self.x

    def draw(self):
        self.sprite.draw()


class SmallObstacle(Obstacle):
    width = 17
    height = 35

    def activate(self, batch: Batch) -> None:
        self.image = pyglet.image.ImageGrid(
            get_dino_image().get_region(228, 100 - 2 - 35, 17 * 6, 35), 1, 6
        ).get_texture_sequence()

        self.sprite = NearestSprite(
            cast(pyglet.image.Texture, random.choice(self.image)),
            -self.image.item_width,
            200,
        )

    def update(self, dt: float, speed: float):
        self.x -= dt * speed
        self.sprite.x = self.x

    def draw(self):
        self.sprite.draw()


class Dino:
    v0: float
    g: float
    y: float
    width: float = 44

    def __init__(self) -> None:
        self.in_jump = False
        self.vel = 0
        self.acc = 0
        self.ground_level = 200
        self.jump_duration = 0.5
        self.y = 0

        self.jump_height = 100
        self.g = self.jump_height / (2 * pow(self.jump_duration / 4, 2))
        self.v0 = pow(2 * self.jump_height * self.g, 1 / 2)

    def activate(self, batch: Batch):
        self.dino_image = pyglet.image.ImageGrid(
            get_dino_image().get_region(848, 100 - 2 - 47, 44 * 4, 47), 1, 4
        ).get_texture_sequence()

        self.sprite = NearestSprite(
            pyglet.image.animation.Animation.from_image_sequence(
                self.dino_image[2:4],
                duration=0.5,
            ),
            0,
            y=self.ground_level,
        )

    def draw(self):
        self.sprite.draw()

    def update(self, dt: float, speed: float):
        for frame in cast(
            list[pyglet.image.AnimationFrame],
            cast(pyglet.image.Animation, self.sprite._animation).frames,
        ):
            frame.duration = pow((speed / 400) + 1, -2)
        self.vel -= self.g * dt
        self.y += self.vel * dt
        if self.y < 0:
            self.y = 0
            self.vel = 0
        self.sprite.y = self.y + self.ground_level

    def jump(self):
        if self.y == 0:
            self.vel = self.v0


class DinoRunner(Scene):
    background: Background
    dino: Dino
    obstacles: list[Obstacle]

    def __init__(self, window: Window) -> None:
        super().__init__(window)
        self.frame = Frame(window, order=4)
        self.batch = None
        self.window = window
        self.background = Background()
        self.dino = Dino()
        self.game_width = 1200

        self.time = 0
        self.should_jump = False

        self.uuid = ""
        self._reset()

    def activate(self) -> None:
        self._reset()

        self.batch = Batch()
        self.background.activate(self.batch)
        for obstacle in self.obstacles:
            obstacle.activate(self.batch)
        self.dino.activate(self.batch)
        self.score = Label(
            f"Score: 0",
            x=int(self.window.width // 2),
            y=self.window.height - 20,
            color=(0, 0, 0, 255),
            anchor_x="center",
            anchor_y="top",
            font_name="Times New Roman",
            font_size=12,
        )
        self.actions: dict[float, list[RunnerAction]] = defaultdict(lambda: [])

    def _reset(self) -> None:
        self.state = 0
        self.speed = 400
        self.acc = 20
        self.offset = 0

        self.obstacles = [
            SmallObstacle(),
            SmallObstacle(),
            SmallObstacle(),
            SmallObstacle(),
            SmallObstacle(),
            SmallObstacle(),
            BigObstacle(),
            BigObstacle(),
            LongObstacle(),
        ]
        for obs in self.obstacles:
            obs.x = -obs.width

        self.dts: list[float] = []

    def draw(self) -> None:
        pyglet.gl.glClearColor(1, 1, 1, 1)
        if self.batch:
            self.batch.draw()
        for obstacle in self.obstacles:
            obstacle.draw()
        self.dino.draw()
        self.score.draw()

    def deactivate(self) -> None:
        return super().deactivate()

    def _on_interact_handler(self, interact: Interact) -> None:
        if interact.status == InteractStatus.INTERACT_STATUS_UPDATE:
            self.rng = random.Random(interact.progress)
            self.time = 0
            self.offset = 0
            self.state = 1

    def on_key_press(self, symbol: int, modifiers: int) -> int | None:
        if symbol == SPACE:
            if self.state == 0:
                client.global_connection.interact(
                    uuid=self.uuid,
                    status=InteractStatus.INTERACT_STATUS_UPDATE,
                    handler=self._on_interact_handler,
                )
            if self.state == 1:
                self.should_jump = True

    def on_key_release(self, symbol: int, modifiers: int) -> int | None:
        if symbol == SPACE:
            self.should_jump = False

    def update(self, dt: float) -> None:
        if self.state == 1:
            self.dts.append(dt)
            self.offset -= self.speed * dt
            self.speed += self.acc * dt
            self.time += dt
            self.background.update(dt, self.offset)
            self.dino.update(dt, self.speed)
            for obstacle in self.obstacles:
                obstacle.update(dt, self.speed)
                if obstacle.x < self.dino.width and obstacle.x + obstacle.width > 0:
                    if self.dino.y < obstacle.height:
                        self.actions[self.time].append(RunnerAction.RUNNER_ACTION_DIE)
                        self.state = 2
            obstacles = sorted(self.obstacles, key=lambda x: cast(int, x.x))
            last = obstacles[-1]
            if last.x + last.width < self.game_width:
                if self.rng.random() < 0.04:
                    free = [x for x in obstacles if x.x + x.width <= 0]
                    if len(free) > 0:
                        obs = self.rng.choice(free)
                        obs.x = self.game_width

            if self.should_jump:
                self.actions[self.time].append(RunnerAction.RUNNER_ACTION_JUMP)
                self.dino.jump()

            self.score.text = f"Score: {int(-self.offset//100):d}"

        if self.state == 2:
            pyglet.gl.glClearColor(0, 0, 0, 1)
            client.global_connection.interact(
                uuid=self.uuid,
                status=InteractStatus.INTERACT_STATUS_STOP,
                runner=Runner(
                    events=[
                        RunnerEvent(time=k, action=a)
                        for k, v in self.actions.items()
                        for a in v
                    ],
                    dts=self.dts,
                ),
            )
            client.scene_manager.set_scene("game")
