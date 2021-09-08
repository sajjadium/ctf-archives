from Rnd import Rnd
from Sprite import Sprite
from Entity import Entity
from Tile import Tile
from Input import KeysPressed
from pygame import Rect
from pygame.sprite import Group
from math import floor
from copy import copy
from Rnd import Rnd
from MrDeath import MrDeath
import pygame

class Spawner(object):
  LEFT = 0
  RIGHT = 1
  SPAWN_THRESHOLD_X = 2000
  SPAWN_THRESHOLD_Y = 600

  def __init__(self, game, player):
    self.game = game
    self.player = player
    self.hasSpawned = False
    self.rnd = Rnd(player)

  def tick(self):
    if not self.hasSpawned and self.player.x >= Spawner.SPAWN_THRESHOLD_X and self.player.y >= Spawner.SPAWN_THRESHOLD_Y:
        # Generate Random Position for enemy
        val = self.rnd.randint(0, 1000)
        enemy = None
        if (val >= 994):
          enemy = MrDeath(self.game.renderer, self.game.map, self.game.playerGroup, 2708, 782-32*2)
        else:
          enemy = MrDeath(self.game.renderer, self.game.map, self.game.playerGroup, 2708.0, 782)
        self.game.tickGroup.add(enemy)
        self.game.enemyGroup.add(enemy)
        self.hasSpawned = True