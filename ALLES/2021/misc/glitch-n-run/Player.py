from Sprite import Sprite
from Entity import Entity
from Tile import Tile
from Input import KeysPressed
from pygame import Rect
from pygame.sprite import Group
from math import floor
from copy import copy
import pygame

class Player(Entity):
  INVENTORY_POS_Y = 450
  INVENTORY_POS_X = 20
  INVENTORY_LENGTH_X = 200
  INVENTORY_LENGTH_Y = 20

  def __init__(self, renderer, input, map, enemyGroup, x, y):
    super(Player, self).__init__(
        renderer, map, 'Android', x, y, Rect(20, 18, 26, 32),
        4, 8, 66, {'die': (4, -2)})
    self.renderer = renderer
    self.input = input
    self.enemyGroup = enemyGroup
    self.prevKeysPressed = KeysPressed()
    self.keysPressed = KeysPressed()
    self.invulnerableTimer = 0
    self.jumpTimer = 0
    self.crouching = False
    self.holdingFlagTimer = 0
    self.inventory = []
    self.map = map
    self.flagsCollected = []
    self.ramDuration = 0
    self.ramSpeed = 0
    self.font = pygame.font.Font(pygame.font.get_default_font(), 24)

  def handleKeypresses(self):
    self.prevKeysPressed = copy(self.keysPressed)
    self.keysPressed = self.input.getKeysPressed()

    if self.isImmobile():
      return

    if self.isRammed():
      self.ramDuration -= 1
      self.x += self.ramSpeed[0]
      self.y += self.ramSpeed[1]
      self.ramSpeed[0] *= 0.9
      self.ramSpeed[1] *= 0.9
      return

    if self.keysPressed.up and not self.prevKeysPressed.up:
      self.jump()
    if self.keysPressed.down and not self.prevKeysPressed.down:
      self.startCrouching()
    elif not self.keysPressed.down and self.prevKeysPressed.down:
      self.stopCrouching()
    if self.keysPressed.right:
      if self.canWalk():
        self.setDirection(Sprite.RIGHT)
        self.startMoving()
    if self.keysPressed.left:
      if self.canWalk():
        self.setDirection(Sprite.LEFT)
        self.startMoving()
    if not self.keysPressed.left and not self.keysPressed.right:
      self.stopMoving()
    if not self.keysPressed.move_inventory_right and self.prevKeysPressed.move_inventory_right:
      self.moveInventory()

  def canWalk(self):
    if self.isImmobile():
      return False
    return True

  def isRammed(self):
    return self.ramDuration > 0

  def isImmobile(self):
    return self.isHoldingFlag() or super(Player, self).isImmobile()

  def isHoldingFlag(self):
    return self.holdingFlagTimer > 0

  def damage(self, amount):
    if self.invulnerableTimer > 0:
      return
    super(Player, self).damage(amount)
    if not self.dead:
      self.invulnerableTimer = 45

  def jump(self):
    # No jumping if you fall too far
    if self.jumpTimer <= 0 and self.y <= 1600:
      self.onGround = False
      self.fallSpeed = -40
      self.jumpTimer = 9

  def startCrouching(self):
    if not self.crouching:
      self.crouching = True
      self.collRect = Rect(20, 32, 26, 18)

  def teleport(self,x,y):
    self.x = x
    self.y = y

  def stopCrouching(self):
    if self.crouching:
      self.crouching = False
      self.collRect = Rect(20, 18, 26, 32)

  def moveInventory(self):
    for currentSlot in range(7,-1,-1):
        isOccupied = False
        for i,item in self.inventory:
          # An item is already on the current slot
          if (currentSlot == i):
            isOccupied = True
          if isOccupied:
            self.inventory.remove((currentSlot,item))
            self.inventory.append((currentSlot+1,item))
            if currentSlot+1 == 8:
              self.dropItem(currentSlot+1)
            return
    

  def getInventoryItemByIndex(self, index):
    for i,item in self.inventory:
      if index == i:
        return (i, item)

    return None

  def dropItem(self, index):
    rect = self.getCollRect()
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    midX = floor(rect.centerx / Tile.LENGTH)
    midY = floor(rect.centery / Tile.LENGTH)
    for offset in offsets:
      x = midX + offset[0]
      y = midY + offset[1]
      tile = self.map.getTile(x, y)
      if tile is not None and tile.id == Tile.EMPTY:
        itemToDrop = self.getInventoryItemByIndex(index)
        self.map.setTile(x, y, itemToDrop[1])
        self.inventory.remove(itemToDrop)
        break
  
  def changeAnimation(self, animation):
    super(Player, self).changeAnimation(animation)

  def updateAnimation(self):
    if self.damageTimer != 0:
      # Damage animation handled in Entity.
      return

    if self.isHoldingFlag():
      self.changeAnimation("hold-flag")
    elif self.onGround:
      if self.moving:
        if self.crouching:
          self.changeAnimation("crouch-walk")
        else:
          self.changeAnimation("walk")
      elif self.crouching:
        self.changeAnimation("crouch")
      else:
        self.changeAnimation("idle")
    else:
      if self.fallSpeed > 0:
        self.changeAnimation("jump-down")
      else:
        self.changeAnimation("jump-up")

  def getNextFreeSlot(self):
    for currentSlot in range(0, 8):
      isFree = True
      for i,item in self.inventory:
        #an item is already on the current slot
        if (currentSlot == i):
          isFree = False
      if isFree:
        return currentSlot
    return None

  def pickUpNearbyOrb(self):
    rect = self.getCollRect()
    for data in self.map.getCloseOrbRects(rect):
      orbRect, x, y = data
      if rect.colliderect(orbRect) and self.keysPressed.space:
        self.map.setTile(x, y, Tile.EMPTY)

        freeSlot = self.getNextFreeSlot()
        if freeSlot == None:
          break
        self.inventory.append((freeSlot,Tile.ORB))
        break

  def pickUpNearbyFlag(self):
    rect = self.getCollRect()
    for data in self.map.getCloseFlagRects(rect):
      flagRect, x, y, flag_id = data
      if rect.colliderect(flagRect):
        self.map.setTile(x, y, Tile.EMPTY)
        if not flag_id in self.flagsCollected:
          self.flagsCollected.append(flag_id)
        break

    rect = self.getCollRect()
    offsets = [(0, 0), (1, 0), (-1, 0)]
    midX = floor(rect.centerx / Tile.LENGTH)
    midY = floor(rect.centery / Tile.LENGTH)

  def render_inventory(self, display):
    text_surface = self.font.render('Inventory:', True, (255, 255, 255))
    display.blit(text_surface, (Player.INVENTORY_POS_X, Player.INVENTORY_POS_Y - 30))

    pygame.draw.rect(display, [255,255,255], (Player.INVENTORY_POS_X,Player.INVENTORY_POS_Y,Player.INVENTORY_LENGTH_X,Player.INVENTORY_LENGTH_Y),2)
    for i in range(0, 8):
      pygame.draw.line(display, [255,255,255], (Player.INVENTORY_POS_X+i*(Player.INVENTORY_LENGTH_X / 8),Player.INVENTORY_POS_Y),(Player.INVENTORY_POS_X+i*(Player.INVENTORY_LENGTH_X / 8),Player.INVENTORY_POS_Y + Player.INVENTORY_LENGTH_Y), 2)

    for i,item in self.inventory:
      self.map.tiles[item].render_absolute(display, Player.INVENTORY_POS_X + 25*i,Player.INVENTORY_POS_Y - Tile.LENGTH /2)

  
  def render(self, display, cameraX, cameraY):
    super(Player, self).render(display, cameraX, cameraY)

    if display == None:
      return
    text_surface = self.font.render(f'Flags {len(self.flagsCollected)} - 6', True, (0, 0, 0))
    display.blit(text_surface, (10, 10))
    self.render_inventory(display)


  def tick(self):
    self.handleKeypresses()

    super(Player, self).tick()

    if (self.y > 10000):
      self.die()

    if self.dead:
      self.visible = True
      return

    self.pickUpNearbyFlag()
    self.pickUpNearbyOrb()

    if self.holdingFlagTimer > 0:
      self.holdingFlagTimer += 1

    if self.invulnerableTimer > 0:
      self.invulnerableTimer -= 1
      if self.damageTimer == 0:
        self.visible = (self.invulnerableTimer / 2) % 2
    else:
      self.visible = True

    if self.jumpTimer > 0:
      self.jumpTimer -= 1

    self.renderer.updateCamera(self.getCollRect())
    self.updateAnimation()