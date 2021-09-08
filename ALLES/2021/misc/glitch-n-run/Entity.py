from Sprite import Sprite

# Common class for the player and enemies
class Entity(Sprite):
  GROUND = 400
  def __init__(self, renderer, map, graphic, x, y, collRect, speed,
               health, flipAdjustment, animationAdjustments):
    x -= collRect.centerx
    y -= collRect.bottom
    super(Entity, self).__init__(
        renderer, graphic, "idle", Sprite.RIGHT, x, y,
        flipAdjustment, animationAdjustments)
    self.map = map
    self.collRect = collRect
    self.speed = speed
    self.health = health
    self.prevCollRect = self.getCollRect()
    self.moving = False
    self.onGround = True
    self.fallSpeed = 0
    self.flying = False
    self.dead = False
    self.damageTimer = 0
    self.collideLeft = False
    self.collideRight = False
    self.collideTop = False
    self.collideBottom = False

  def getCollRect(self):
    return self.collRect.move(self.x, self.y)

  def changeAnimation(self, animation, stayOnSameFrame = False):
    if self.animation != animation:
      self.setAnimation(animation, stayOnSameFrame)

  def startMoving(self):
    self.moving = True
  def stopMoving(self):
    self.moving = False

  def startFalling(self):
    self.onGround = False
  def stopFalling(self):
    self.onGround = True
    self.fallSpeed = 0

  def damage(self, amount):
    if not self.dead:
      self.health -= amount
      if self.health <= 0:
        self.die()
      else:
        self.damageTimer = 8

  def die(self):
    self.dead = True

  def destroy(self):
    self.kill() # Cleans up the pygame.sprite.

  def isDamaged(self):
    return self.damageTimer > 0

  def isImmobile(self):
    return self.dead or self.isDamaged()

  def handleCollision(self):
    self.collideLeft = False
    self.collideRight = False
    self.collideTop = False
    self.collideBottom = False

    rect = self.getCollRect()
    prevRect = self.prevCollRect

    for tileRect in self.map.getCloseSolidCollRects(rect):
      if tileRect.left < rect.right and tileRect.right > rect.left:
        if (tileRect.top <= rect.bottom + 1
            and tileRect.top >= prevRect.bottom - 1):
          rect.bottom = tileRect.top
          self.collideBottom = True
        elif (tileRect.bottom >= rect.top - 1
              and tileRect.bottom <= prevRect.top + 1):
          rect.top = tileRect.bottom
          self.collideTop = True
      if tileRect.top < rect.bottom and tileRect.bottom > rect.top:
        if (tileRect.left <= rect.right + 1
            and tileRect.left >= prevRect.right - 1):
          rect.right = tileRect.left
          self.collideRight = True
        elif (tileRect.right >= rect.left - 1
              and tileRect.right <= prevRect.left + 1):
          rect.left = tileRect.right
          self.collideLeft = True

    self.x += rect.x - self.getCollRect().x
    self.y += rect.y - self.getCollRect().y

    for spikeRect in self.map.getCloseSpikeDamageRects(rect):
      if spikeRect.colliderect(rect):
        self.damage(1000)
        break

    self.prevCollRect = self.getCollRect()

  def tick(self):
    if self.dead:
      if self.animation == "die" and self.finishedAnimation():
        self.destroy()
      else:
        self.changeAnimation("die")
    elif self.isDamaged():
      self.changeAnimation("damaged")

    if not self.isImmobile():
      if not self.onGround:
        if not self.flying:
          if self.collideTop and self.fallSpeed < 0:
            self.fallSpeed = 2 # Bump into ceiling
          self.y += self.fallSpeed
          self.fallSpeed = self.fallSpeed + 5
      if self.moving:
        if self.direction == Sprite.LEFT and not self.collideLeft:
          self.x -= self.speed
        elif self.direction == Sprite.RIGHT and not self.collideRight:
          self.x += self.speed

    self.handleCollision()

    if not self.collideBottom:
      self.startFalling()
    else:
      self.stopFalling()

    if self.damageTimer > 0:
      self.damageTimer -= 1
