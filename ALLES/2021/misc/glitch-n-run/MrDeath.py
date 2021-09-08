from Sprite import Sprite
from Enemy import Enemy
from Tile import Tile
from pygame import Rect
import pygame
import math

class MrDeath(Enemy):
  def __init__(self, renderer, map, playerGroup, x, y):
    super(MrDeath, self).__init__(
        renderer, map, playerGroup, 'MrDeath',
        x, y, Rect(4, 2, 22, 32), 10, 2, 32, {})
    self.t = 0
    self.setDirection(Sprite.LEFT)
    self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
    self.state = "IDLE"

  def startRunning(self):
    self.moving = True

  def tick(self):
    super(MrDeath, self).tick()

    if self.isImmobile():
      return

    if len(self.playerGroup.sprites()) == 0:
      return

    player = self.playerGroup.sprites()[0]
    if math.hypot(self.x-player.x, self.y-player.y) < 100 and abs(self.y-player.y) < 20:
        self.startRunning()

    self.t += 1

  def render(self, display, cameraX, cameraY):
    super(MrDeath, self).render(display, cameraX, cameraY)

    for rect in self.getDamageRects():
      for player in self.playerGroup.sprites():
        if player.getCollRect().colliderect(rect):
          player.die()