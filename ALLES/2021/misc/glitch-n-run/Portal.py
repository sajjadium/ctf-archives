from Sprite import Sprite
from Enemy import Enemy
from Tile import Tile
from pygame import Rect
import pygame
import math
from Entity import Entity

class Portal(Enemy):
  def __init__(self, renderer, map, playerGroup, x, y, destination):
    super(Portal, self).__init__(
        renderer, map, playerGroup, 'Portal',
        x, y, Rect(0, 0, 32, 48), 10, 2, 32, {})
    self.t = 0
    self.state = "IDLE"
    self.destination = destination
    self.enabled = True

  def tick(self):
    if not self.enabled:
        return

    for rect in self.getDamageRects():
      for player in self.playerGroup.sprites():
        if player.getCollRect().colliderect(rect):
            self.enabled = False
            player.teleport(self.destination[0], self.destination[1])


  def render(self, display, cameraX, cameraY):
   super(Portal, self).render(display, cameraX, cameraY)
