from Sprite import Sprite
from Enemy import Enemy
from Tile import Tile
from pygame import Rect
from LiveOverflowProjectile import LiveOverflowProjectile
import pygame
import math

class MrHacker(Enemy):
  def __init__(self, renderer, map, playerGroup, x, y):
    super(MrHacker, self).__init__(
        renderer, map, playerGroup, 'MrHacker',
        x, y, Rect(4, 2, 22, 32), 10, 2, 32, {})
    self.t = 0
    self.renderer = renderer
    self.setDirection(Sprite.LEFT)
    self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
    self.state = "IDLE"
    self.shootTimer = -1
    self.projectiles = []
    self.cooldown = 0

  def startRunning(self):
    self.moving = True

  def shoot(self):
    self.state = "SHOOT"
    self.changeAnimation("shoot") 
    offset = 0 if self.direction == Sprite.LEFT else 32
    direction =  -6 if self.direction == Sprite.LEFT else 6
    self.projectiles.append(LiveOverflowProjectile(self.renderer, self.map, self.playerGroup, self.x + offset, self.y+ 24, (direction,0)))
    self.shootTimer = 0
    self.cooldown = 60

  def tick(self):
    super(MrHacker, self).tick()

    if self.isImmobile():
      return

    if len(self.playerGroup.sprites()) == 0:
      return

    if self.shootTimer >= 0:
      self.shootTimer += 1
    
    if self.shootTimer >= 3:
      self.shootTimer = -1
      self.state = "IDLE"
      self.changeAnimation("idle") 

    if self.cooldown > 0:
      self.cooldown -= 1

    player = self.playerGroup.sprites()[0]
    if abs(self.y - player.y) <= 32 and self.cooldown == 0 and math.hypot(self.x-player.x, self.y-player.y) < 400:
      self.shoot()

    if (self.x >= player.x):
      self.setDirection(Sprite.LEFT)
    else:
      self.setDirection(Sprite.RIGHT)

    for projectile in self.projectiles:
      projectile.tick()

    self.t += 1

  def render(self, display, cameraX, cameraY):
    super(MrHacker, self).render(display, cameraX, cameraY)

    for projectile in self.projectiles:
      projectile.render(display, cameraX, cameraY)
