from Sprite import Sprite
from Enemy import Enemy
from Tile import Tile
from pygame import Rect
import pygame
import math
from Entity import Entity

class LiveOverflowProjectile(Enemy):
  def __init__(self, renderer, map, playerGroup, x, y, velocity):
    super(LiveOverflowProjectile, self).__init__(
        renderer, map, playerGroup, 'LiveOverflowProjectile',
        x, y, Rect(0, 0, 32, 32), 10, 2, 32, {})
    self.t = 0
    self.state = "IDLE"
    self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
    self.enabled = True
    self.velocity = velocity

  def tick(self):
    if not self.enabled:
        return
    
    self.x += self.velocity[0]
    self.y += self.velocity[1]

    for rect in self.getDamageRects():
      for player in self.playerGroup.sprites():
        if player.getCollRect().colliderect(rect):
          self.enabled = False
          player.ramDuration = 30
          player.ramSpeed = [40 * math.copysign(1, self.velocity[0]), -25]


  def render(self, display, cameraX, cameraY):
      if self.enabled:
            super(LiveOverflowProjectile, self).render(display, cameraX, cameraY)
