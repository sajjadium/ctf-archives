import pygame

class Tile(object):
  LENGTH = 32
  SPIKE_LENGTH = 12
  NUM_TILES = 32

  EMPTY = 0
  WALL = 1
  SPIKE_U = 2
  SPIKE_D = 3
  SPIKE_L = 4
  SPIKE_R = 5
  RND_SPIKE_U = 7
  RND_SPIKE_D = 8
  ORB = 11
  FLAG = 12
  PLAYER_SPAWN = 20
  DEATH_SPAWN = 21
  IE_SPAWN = 15
  T_REX_SPAWN = 16
  HALFWALL = 14
  MRHACKER_SPAWN = 22
  PORTAL = 23
  FLAG_1 = 25
  FLAG_2 = 26
  FLAG_3 = 27
  FLAG_4 = 28
  FLAG_5 = 29
  FLAG_6 = 30
  FLAG_7 = 31

  def __init__(self, id, image):
    self.id = id
    self.image = image

  def isSolid(self):
    return (self.id == Tile.WALL or self.id == Tile.HALFWALL or self.isSpike() or self.id >= 32)

  def isSpike(self):
    return (self.id == Tile.SPIKE_U or self.id == Tile.SPIKE_D
            or self.id == Tile.SPIKE_L or self.id == Tile.SPIKE_R
            or self.id == Tile.RND_SPIKE_U
            or self.id == Tile.RND_SPIKE_D)

  def isEnemySpawn(self):
    return (self.id == Tile.DEATH_SPAWN or self.id == Tile.MRHACKER_SPAWN or self.id == Tile.PORTAL)

  def render(self, display, x, y, cameraX, cameraY):
    if self.image:
      display.blit(
          self.image, (x * Tile.LENGTH - cameraX, y * Tile.LENGTH - cameraY))

  def render_absolute(self, display, x, y):
    if self.image:
      display.blit(
          self.image, (x, y))

  def getCollRect(self):
    if (self.id == Tile.SPIKE_U
        or self.id == Tile.RND_SPIKE_U):
      return pygame.Rect(0, Tile.LENGTH - Tile.SPIKE_LENGTH,
                         Tile.LENGTH, Tile.SPIKE_LENGTH)
    elif self.id == Tile.SPIKE_D or self.id == Tile.RND_SPIKE_D:
      return pygame.Rect(0, 0, Tile.LENGTH, Tile.SPIKE_LENGTH)
    elif self.id == Tile.SPIKE_L:
      return pygame.Rect(Tile.LENGTH - Tile.SPIKE_LENGTH, 0,
                         Tile.SPIKE_LENGTH, Tile.LENGTH)
    elif self.id == Tile.SPIKE_R:
      return pygame.Rect(0, 0, Tile.SPIKE_LENGTH, Tile.LENGTH)
    elif self.id == Tile.FLAG:
      return pygame.Rect(13, 18, 11, 14)
    elif self.id == Tile.HALFWALL:
      return pygame.Rect(0, 0, 8, 32)
    return pygame.Rect(0, 0, Tile.LENGTH, Tile.LENGTH)

  def getDamageRect(self):
    if (self.id == Tile.SPIKE_U
        or self.id == Tile.RND_SPIKE_U):
      return pygame.Rect(1, Tile.LENGTH - Tile.SPIKE_LENGTH - 1,
                         Tile.LENGTH - 2, 0)
    elif self.id == Tile.SPIKE_D or self.id == Tile.RND_SPIKE_D:
      return pygame.Rect(1, Tile.SPIKE_LENGTH + 1, Tile.LENGTH - 2, 0)
    elif self.id == Tile.SPIKE_L:
      return pygame.Rect(Tile.LENGTH - Tile.SPIKE_LENGTH - 1, 1,
                         0, Tile.LENGTH - 2)
    elif self.id == Tile.SPIKE_R:
      return pygame.Rect(Tile.SPIKE_LENGTH + 1, 1, 0, Tile.LENGTH - 2)
    return pygame.Rect(0, 0, Tile.LENGTH, Tile.LENGTH)
