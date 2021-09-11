
ZOOM_MIN = -8
ZOOM_MAX = -3

class Camera(object):
    x: float
    y: float
    zoom_level: int

    def __init__(self, x, y, zoom_level):
        self.x = x
        self.y = y
        self.zoom_level = zoom_level

    def zoom_in(self):
        self.zoom_level = min(self.zoom_level + 1, ZOOM_MAX)

    def zoom_out(self):
        self.zoom_level = max(self.zoom_level - 1, ZOOM_MIN)

    def follow_player(self, player, dt):
        tx = player.x + 0.5
        ty = player.y + 0.5
        self.x = (self.x * 0.9) + (tx * 0.1)
        self.y = (self.y * 0.9) + (ty * 0.1)

    @property
    def zoom(self):
        return pow(2, self.zoom_level)
