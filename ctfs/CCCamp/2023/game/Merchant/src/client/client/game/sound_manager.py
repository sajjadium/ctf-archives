import pyglet


class SoundManager:
    def __init__(self) -> None:
        self.player = pyglet.media.Player()
        self.bg_music = None
        pass

    def set_background_music(self, path: str) -> None:
        self.bg_music = pyglet.resource.media(path)
        self.player.queue(self.bg_music)
        pass

    def play_background_music(self) -> None:
        if self.bg_music is None:
            return

        self.player.play()

    def stop_background_music(self) -> None:
        self.player.pause()
