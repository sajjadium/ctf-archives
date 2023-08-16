from dataclasses import dataclass


@dataclass
class Renderable:
    is_loaded: bool
    is_ready: bool

    def __init__(self) -> None:
        self.is_ready = False
        self.is_loaded = False

    def on_load(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        if not self.is_loaded and self.is_ready:
            self.on_load()

            self.is_loaded = True
