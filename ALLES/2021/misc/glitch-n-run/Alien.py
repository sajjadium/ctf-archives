from Sprite import Sprite
from Enemy import Enemy
from Tile import Tile
from pygame import Rect
import pygame
import math
from Entity import Entity

class Alien(Enemy):
  START_X = 3730
  START_Y = 2000
  def __init__(self, renderer, map, playerGroup, x, y):
    super(Alien, self).__init__(
        renderer, map, playerGroup, 'MysteriousThing',
        x, y, Rect(4, 2, 50, 150), 10, 2, 32, {})
    self.t = 0
    self.state = "IDLE"
    self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
    self.enabled = True

  def tick(self):
    if not self.enabled:
        return

    self.t += 1
    x = Alien.START_X + 800*math.sin(5*self.t*math.pi/180)
    self.x = x
    for rect in self.getDamageRects():
      for player in self.playerGroup.sprites():
        if player.getCollRect().colliderect(rect):
            freeSlot = player.getNextFreeSlot()
            player.inventory.append((freeSlot,Tile.FLAG_5))
            player.fallSpeed = 0
            player.teleport(1490.0, 900)
            self.enabled = False

  def render(self, display, cameraX, cameraY):
    if display == None:
      return
    text_surface = self.font.render(f'??????', True, (0, 0, 0))
    display.blit(text_surface, (self.getCollRect().move(-cameraX, -cameraY).x, self.getCollRect().move(-cameraX, -cameraY).y))
