from GIFImage import GIFImage
from os import listdir
from os.path import isfile, join
import pygame


class Sprite(pygame.sprite.Sprite):
  LEFT = 0
  RIGHT = 1

  def __init__(self, renderer, graphic, animation, direction, x, y,
               flipAdjustment, animationAdjustments):
    super(Sprite, self).__init__()
    renderer.sprites.add(self)
    self.animation = animation
    self.direction = direction
    self.x = x
    self.y = y
    self.flipped = False
    self.animationAdjustments = animationAdjustments
    self.flipAdjustment = flipAdjustment
    self.animations = {}
    self.visible = True
    path = 'Graphics/Sprites/'+graphic+'/'
    gifs = [f for f in listdir(path)
            if isfile(join(path, f)) and f.endswith('.gif')]
    for gif in gifs:
      name = gif[:-4]
      self.animations[name] = []
      self.animations[name].append(GIFImage(join(path, gif), True))
      self.animations[name].append(GIFImage(join(path, gif), False))

  def setAnimation(self, animation, stayOnSameFrame = False):
    if animation in self.animations:
      cur = self.animations[self.animation][self.direction].cur
      frameTime = self.animations[self.animation][self.direction].frameTime
      self.animation = animation
      if stayOnSameFrame:
        self.animations[self.animation][self.direction].cur = cur
        self.animations[self.animation][self.direction].frameTime = frameTime
      else:
        self.animations[self.animation][Sprite.RIGHT].reset()
        self.animations[self.animation][Sprite.LEFT].reset()

  def setDirection(self, direction):
    if direction != self.direction:
      self.direction = direction

  def render(self, display, cameraX, cameraY):
    if self.animation in self.animations:
      adjx = 0
      adjy = 0
      if self.animation in self.animationAdjustments:
        if self.direction == Sprite.RIGHT:
          adjx = self.animationAdjustments[self.animation][0]
        else:
          adjx = -self.animationAdjustments[self.animation][0]
        adjy = self.animationAdjustments[self.animation][1]
      if self.direction == Sprite.LEFT:
        img = self.animations[self.animation][self.direction].frames[0][0]
        if img is not None:
          adjx -= img.get_width()
        adjx += self.flipAdjustment
      self.animations[self.animation][self.direction].render(
          display, (self.x + adjx - cameraX, self.y + adjy - cameraY),
          self.visible)

  def finishedAnimation(self):
    gifimage =  self.animations[self.animation][self.direction]
    return not gifimage.loops and gifimage.cur >= gifimage.breakpoint
