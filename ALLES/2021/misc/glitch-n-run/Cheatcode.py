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
import pygame
import hashlib

class Cheatcode(object):
  NUMBER_OF_INPUTS = 7

  def __init__(self, player, input):
    self.player = player
    self.input = input
    self.tick_counter = 0
    self.last_inputs = [0]*Cheatcode.NUMBER_OF_INPUTS
    self.enabled = True

  def tick(self):
    if not self.enabled:
        return

    self.last_inputs[self.tick_counter % Cheatcode.NUMBER_OF_INPUTS] = self.input.getKeysPressed().asNumber()
    self.tick_counter += 1

    hash = hashlib.md5(bytes(self.last_inputs)).hexdigest()
    if hash == 'f869ac552252db7c3dd5a038f63acc3f':
        freeSlot = self.player.getNextFreeSlot()
        self.player.inventory.append((freeSlot,Tile.FLAG_6))
        self.enabled = False