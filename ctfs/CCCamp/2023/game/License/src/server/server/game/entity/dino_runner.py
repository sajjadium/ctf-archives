import random
from collections import defaultdict

from shared.constants import TARGET_UPS
from shared.gen.messages.v1 import Runner, RunnerAction


class Obstacle:
    x: float = 0
    width: float
    height: float


class SmallObstacle(Obstacle):
    width = 17
    height = 35


class BigObstacle(Obstacle):
    width = 25
    height = 50 - 2


class LongObstacle(Obstacle):
    width = 75
    height = 50 - 2


class Engine:
    time: float
    acc: float
    speed: float
    game_width: float
    obstacles: list[Obstacle]
    dino_y: float = 0
    dino_width: float = 44
    dino_v: float = 0
    stop: bool
    seed: float = 0
    rng: random.Random

    def update(self, dt: float):
        self.offset -= self.speed * dt
        self.speed += self.acc * dt
        self.dino_v -= self.g * dt
        self.dino_y += self.dino_v * dt
        if self.dino_y < 0:
            self.dino_y = 0
            self.dino_v = 0
        for obstacle in self.obstacles:
            obstacle.x -= dt * self.speed
            if (
                obstacle.x + obstacle.width >= 0
                and obstacle.x + obstacle.width < self.dino_width
            ):
                if self.dino_y < obstacle.height:
                    self.stop = True

        obstacles = sorted(self.obstacles, key=lambda x: x.x)
        last = obstacles[-1]
        if last.x + last.width < self.game_width:
            if self.rng.random() < 0.04:
                free = [x for x in obstacles if x.x + x.width <= 0]
                if len(free) > 0:
                    obs = self.rng.choice(free)
                    obs.x = self.game_width

    def run(self, runner: Runner):
        self.rng = random.Random(self.seed)
        self.time = 0
        self.acc = 20
        self.speed = 400
        self.game_width = 1200
        self.jump_duration = 0.5
        self.jump_height = 100
        self.offset = 0
        self.g = self.jump_height / (2 * pow(self.jump_duration / 4, 2))
        self.v0 = pow(2 * self.jump_height * self.g, 1 / 2)
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
        self.stop = False
        events: dict[float, list[RunnerAction]] = defaultdict(lambda: [])
        for event in runner.events:
            events[event.time].append(event.action)

        for dt in runner.dts:
            # TODO check that client doesn't cheat by sending weird dts
            if dt > 1 / (10) or dt < 1 / (TARGET_UPS * 1.2):
                return False, self.time, int(-self.offset // 100)

            self.time += dt
            self.update(dt)
            if self.stop:
                if RunnerAction.RUNNER_ACTION_DIE in events[self.time]:
                    break
                return False, self.time, int(-self.offset // 100)
            for action in events[self.time]:
                if action == RunnerAction.RUNNER_ACTION_JUMP:
                    if self.dino_y == 0:
                        self.dino_v = self.v0
        return True, self.time, int(-self.offset // 100)
