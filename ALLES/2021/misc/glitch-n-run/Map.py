import pygame

from math import floor, ceil

from Tile import Tile

class Map(pygame.sprite.Sprite):
  def __init__(self, renderer, mode):
    super(Map, self).__init__()
    self.renderer = renderer
    self.mode = mode
    self.tiles = self.loadTiles()
    self.map = self.loadMap()
    renderer.sprites.add(self)

  def loadTiles(self):
    tiles = {}
    tileset_image = pygame.image.load("Graphics/tileset.png")
    if (tileset_image.get_width() % Tile.LENGTH != 0
        or tileset_image.get_height() % Tile.LENGTH != 0):
      exit(1)
    tile_id = 0
    for y in range(int(tileset_image.get_height() / Tile.LENGTH)):
      for x in range(int(tileset_image.get_width() / Tile.LENGTH)):
        rect = (x*Tile.LENGTH, y*Tile.LENGTH, Tile.LENGTH, Tile.LENGTH)
        tile_image = tileset_image.subsurface(rect)
        tiles[tile_id] = Tile(tile_id, tile_image)
        tile_id += 1
    return tiles

  def loadMap(self):
    map = []
    with open("Map/map.txt") as f:
      map_text =  f.read()

    for line in map_text.strip().split("\n"):
      map_line = []
      for chunk in line.strip().split(","):
        map_line.append(int(chunk))
      map.append(map_line)
    return map

  def getPlayerStartPos(self):
    for y in range(len(self.map)):
      for x in range(len(self.map[0])):
        if self.tiles[self.map[y][x]].id == Tile.PLAYER_SPAWN:
          return (x * Tile.LENGTH + Tile.LENGTH / 2, (y + 1) * Tile.LENGTH)
    return None

  def getEnemyStartPos(self):
    result = []
    for y in range(len(self.map)):
      for x in range(len(self.map[0])):
        tile = self.tiles[self.map[y][x]]
        if tile.isEnemySpawn():
          result.append((x * Tile.LENGTH + Tile.LENGTH / 2,
                         (y + 1) * Tile.LENGTH, tile.id))
    return result


  def render(self, display, cameraX, cameraY):
    for y in range(len(self.map)):
      for x in range(len(self.map[0])):
        tile = self.tiles[self.map[y][x]]
        if display == None:
          continue

        tile.render(display, x, y, cameraX, cameraY)

  def getTile(self, x, y):
    if x < 0 or y < 0 or x >= len(self.map[0]) or y >= len(self.map):
      return None
    return self.tiles[self.map[y][x]]

  def setTile(self, x, y, id):
    if x < 0 or y < 0 or x >= len(self.map[0]) or y >= len(self.map):
      return
    self.map[y][x] = id

  def getCloseTileCollRects(self, rect, id):
    result = []
    for x in range(floor(rect.left/Tile.LENGTH) - 1,
                   ceil(rect.right/Tile.LENGTH) + 1):
      for y in range(floor(rect.top/Tile.LENGTH) - 1,
                     ceil(rect.bottom/Tile.LENGTH) + 1):
        if x >= 0 and y >= 0 and x < len(self.map[0]) and y < len(self.map):
          tile = self.tiles[self.map[y][x]]
          if id == "solid" and tile.isSolid():
            result.append(tile.getCollRect().move(x*Tile.LENGTH, y*Tile.LENGTH))
          elif id == "spike" and tile.isSpike():
            result.append(
                tile.getDamageRect().move(x*Tile.LENGTH, y*Tile.LENGTH))
          elif ((id == "orb" and tile.id == Tile.ORB)):
            result.append((
                tile.getCollRect().move(x*Tile.LENGTH, y*Tile.LENGTH),
                x, y))
          elif (id == "flag" and (tile.id == Tile.FLAG_1 or tile.id == Tile.FLAG_2
           or tile.id == Tile.FLAG_3  or tile.id == Tile.FLAG_4  or tile.id == Tile.FLAG_5
            or tile.id == Tile.FLAG_6  or tile.id == Tile.FLAG_7)):
            result.append((
                tile.getCollRect().move(x*Tile.LENGTH, y*Tile.LENGTH),
                x, y, tile.id))
    return result

  def getCloseSolidCollRects(self, rect):
    return self.getCloseTileCollRects(rect, "solid")

  def getCloseSpikeDamageRects(self, rect):
    return self.getCloseTileCollRects(rect, "spike")

  def getCloseFlagRects(self, rect):
    return self.getCloseTileCollRects(rect, "flag")

  def getCloseOrbRects(self, rect):
    return self.getCloseTileCollRects(rect, "orb")


  def tick(self):
    pass
