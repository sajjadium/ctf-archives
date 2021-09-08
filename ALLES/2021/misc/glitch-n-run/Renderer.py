import pygame
from Sprite import Sprite
from Tile import Tile
from pygame import Rect
import os
import zlib

class Renderer(object):
  W = 640
  H = 480

  def __init__(self, mode):
    self.mode = mode
    self.frameCount = 0
    if self.mode == "check":
      self.display = None
    else:
      self.display = pygame.display.set_mode((Renderer.W, Renderer.H), 0, 32)
      pygame.display.set_caption('ALLESCTF! KotH Challenge')
      self.bg = pygame.image.load('Graphics/bg.png')
    self.sprites = pygame.sprite.Group()
    self.cameraX = 0
    self.cameraY = 0


  def updateCamera(self, playerRect):
    self.cameraX = playerRect.centerx - Renderer.W / 2
    self.cameraY = playerRect.bottom - Renderer.H* 2 / 3

  def tileIsInView(self, x, y):
    tileRect = Rect(x * Tile.LENGTH - Tile.LENGTH,
                    y * Tile.LENGTH - Tile.LENGTH,
                    Tile.LENGTH * 2,
                    Tile.LENGTH * 2)
    cameraRect = Rect(self.cameraX, self.cameraY, Renderer.W, Renderer.H)
    return tileRect.colliderect(cameraRect)

  def render(self):
    if self.mode == "check":
      # We still call the sprites' render function so that
      # the animation progresses.
      for sprite in self.sprites.sprites():
        sprite.render(None, self.cameraX, self.cameraY)

      self.frameCount += 1
      return 
    # Draw BG
    bgX = -(self.cameraX % self.bg.get_width())
    bgY = -(self.cameraY % self.bg.get_height())
    for x in range(0, Renderer.W + self.bg.get_width(), self.bg.get_width()):
      for y in range(0,
                     Renderer.H + self.bg.get_height(), self.bg.get_height()):
        self.display.blit(self.bg, (x+bgX, y+bgY))

    # Draw sprites
    for sprite in self.sprites.sprites():
      sprite.render(self.display, self.cameraX, self.cameraY)


    pygame.display.flip()