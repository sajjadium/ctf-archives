
import os
# pygame pls, don't spam my stdout :(
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
from Map import Map
from Renderer import Renderer
from Player import Player
from Tile import Tile
from Input import Input
from Spawner import Spawner
from Cheatcode import Cheatcode
import glob
from Portal import Portal
from Alien import Alien
from MrHacker import MrHacker
from Cheatcode import Cheatcode
from MrDeath import MrDeath
import subprocess

class Game(object):
  FPS = 30
  MAX_TICKS = 3200

  def manual(self):
    Game.FPS = 30

  def __init__(self, mode):

    self.mode = mode
    replay = []
    if self.mode == "replay" or self.mode == "check":
      replay = self.loadReplay()
      if self.mode == "replay":
        print("replaying...", flush=True)
        Game.FPS = 200
      else:
        print("checking...", flush=True)
        Game.FPS = 200

    pygame.init()

    self.fpsClock = pygame.time.Clock()
    self.renderer = Renderer(self.mode)
    self.tickGroup = pygame.sprite.Group()
    self.playerGroup = pygame.sprite.Group()
    self.enemyGroup = pygame.sprite.Group()
    self.input = Input(self.mode, replay, lambda: self.manual())
    self.map = Map(self.renderer, self.mode)
    self.spawnEntities()

    self.spawner = Spawner(self, self.playerGroup.sprites()[0])
    self.cheatcode = Cheatcode(self.playerGroup.sprites()[0], self.input)

  def __del__(self):
    pygame.quit()
    if (self.mode == "game" or self.mode == 'replay'):
      self.writeReplayFile("replay.txt")
      print("Wrote replay input to replay.txt", flush=True)

  def loadReplay(self):
    result = []
    try:
      print("Input replay file + empty line", flush=True)
      for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
          break
        result.append(int(line[:6], 2))
        if len(result) > 10000:
           raise "Input too long"
      if len(result) == 0:
        raise "Input empty"
    except:
      print("Bad input :C", flush=True)
      exit(1)
    return result


  def spawnEntities(self):
    x, y = self.map.getPlayerStartPos()
    player = Player(self.renderer, self.input, self.map, self.enemyGroup, x, y)
    self.tickGroup.add(player)
    self.playerGroup.add(player)

    for data in self.map.getEnemyStartPos():
      x, y, type = data
      if type == Tile.DEATH_SPAWN:
        enemy = MrDeath(self.renderer, self.map, self.playerGroup, x, y)
      elif type == Tile.MRHACKER_SPAWN:
        enemy = MrHacker(self.renderer, self.map, self.playerGroup, x, y)
      elif type == Tile.PORTAL:
        pass
      else:
        raise Exception("No such enemy")
      self.tickGroup.add(enemy)
      self.enemyGroup.add(enemy)

    self.tickGroup.add(Alien(self.renderer, self.map, self.playerGroup, Alien.START_X, Alien.START_Y))
    self.tickGroup.add(Portal(self.renderer, self.map, self.playerGroup, 1490.0, 1100, (1490.0, 900)))
    self.tickGroup.add(Portal(self.renderer, self.map, self.playerGroup, 1840.0, 1358, (1490.0, 900)))

  def tick(self):
    if self.mode == "check":
      events = []
    else:
      events = pygame.event.get()
      for event in events:
        if event.type == pygame.locals.QUIT:
          return False

    self.input.tick(events)
    self.spawner.tick()
    for sprite in self.tickGroup.sprites():
      sprite.tick()
    self.map.tick()
    self.renderer.render()
    self.cheatcode.tick()

    if self.mode != "check":
      self.fpsClock.tick(Game.FPS)

    if self.won() or self.died() or self.reachedEndOfReplay():
      return False
    return True

  def won(self):
    if len(self.playerGroup.sprites()) == 0:
      return False
    return len(self.playerGroup.sprites()[0].flagsCollected) == 6 and self.input.pos < Game.MAX_TICKS

  def died(self):
    return len(self.playerGroup.sprites()) == 0

  def reachedEndOfReplay(self):
    return self.input.reachedEndOfReplay()

  def writeReplayFile(self, path):
    self.input.writeReplayFile(path)

  def getCompletionTime(self):
    return self.input.pos
