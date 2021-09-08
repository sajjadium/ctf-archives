from pygame import locals
from copy import copy

class KeysPressed():
  def __init__(self, num=0):
    self.up = True if num & 1 else False
    self.down = True if num & 2 else False
    self.left = True if num & 4 else False
    self.right = True if num & 8 else False
    self.space = True if num & 16 else False
    self.move_inventory_right = True if num & 32 else False

  def asNumber(self):
    num = 1 if self .up else 0
    num |= (1 << 1) if self.down else 0
    num |= (1 << 2) if self.left else 0
    num |= (1 << 3) if self.right else 0
    num |= (1 << 4) if self.space else 0
    num |= (1 << 5) if self.move_inventory_right else 0
    return num

class Input(object):

  def __init__(self, mode, replay, f):
    self.mode = mode
    self.replay = replay
    self.keysPressed = KeysPressed()
    self.pos = 0
    self.prev_progress = 0
    self.manual = f

  def tick(self, events):
    for event in events:
      if event.type == locals.KEYUP or event.type == locals.KEYDOWN:
        pressed = (event.type == locals.KEYDOWN)
        if event.key == locals.K_p:
          print("switching to manual play")
          self.manual()
          self.mode = 'game'
    if self.mode == "game":
      self.readInputFromKeyboard(events)
    else:
      self.readInputFromReplay()

  def readInputFromKeyboard(self, events):
    prevLeft = self.keysPressed.left
    for event in events:
      if event.type == locals.KEYUP or event.type == locals.KEYDOWN:
        pressed = (event.type == locals.KEYDOWN)
        if event.key == locals.K_UP:
          self.keysPressed.up = pressed
        if event.key == locals.K_DOWN:
          self.keysPressed.down = pressed
        if event.key == locals.K_LEFT:
          self.keysPressed.left = pressed
        if event.key == locals.K_RIGHT:
          self.keysPressed.right = pressed
        if event.key == locals.K_SPACE:
          self.keysPressed.space = pressed
        if event.key == locals.K_a:
          self.keysPressed.move_inventory_right = pressed

    # If both directions are pressed, use whichever was pressed most recently.
    if self.keysPressed.left and self.keysPressed.right:
      if prevLeft:
        self.keysPressed.left = False
      else:
        self.keysPressed.right = False

    self.replay.append(copy(self.keysPressed))

  def readInputFromReplay(self):
    keys = self.replay[self.pos] if self.pos < len(self.replay) else 0
    self.pos += 1
    self.keysPressed = KeysPressed(keys)
    if self.mode == "check" or self.mode == "replay":
      progress = round(self.pos / len(self.replay) * 100)
      if self.prev_progress != progress:
        print("%d%%" % progress, flush=True)
        self.prev_progress = progress
    else:
      self.replay.append(copy(self.keysPressed))


  def reachedEndOfReplay(self):
    return self.mode != "game" and self.pos >= len(self.replay)

  def getKeysPressed(self):
    return copy(self.keysPressed)

  def writeReplayFile(self, path):
    txt = ""
    for keys in self.replay:
      if not isinstance(keys, int):
        txt += "{0:06b}\n".format(keys.asNumber())

    with open(path, "w") as f:
      f.write(txt)
