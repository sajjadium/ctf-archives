# Custom random generator that's deterministic.
class Rnd(object):

  def __init__(self, player):
    self.player = player
    self.val = 4
    pass

  def randint(self, min, max):
    # LCG influenced by the inventory.

    # Reset LGC
    self.val = 4
    num = 0
    for i,item in self.player.inventory:
      num |= ( 1 << i)

    for i in range(num + 1):
      self.val = ((self.val * 214013) + 2531013) & 0x7fffffff

    return (self.val % (max - min + 1)) + min 