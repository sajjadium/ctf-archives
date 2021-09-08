# Taken from https://www.pygame.org/project-GIFImage-1039-.html
# Added some minor modifications to time stuff better and detect
# whether a GIF loops.

"""GIFImage by Matthew Roe"""

from PIL import Image
import pygame
from pygame.locals import *

FPS = 30

class GIFImage(object):
    imageCache = {}

    def __init__(self, filename, flipped):
        self.filename = filename
        self.flipped = flipped
        if filename not in GIFImage.imageCache:
          GIFImage.imageCache[filename] = Image.open(filename)
        self.image = GIFImage.imageCache[filename]
        self.frames = []
        self.loops = False
        self.get_frames()

        self.cur = 0
        self.frameTime = 0

        self.running = True
        self.breakpoint = len(self.frames)-1
        self.startpoint = 0
        self.reversed = False

    def get_rect(self):
        return pygame.rect.Rect((0,0), self.image.size)

    def get_frames(self):
        image = self.image

        pal = image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i+3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not image.tile:
                    image.seek(0)
                if image.tile:
                    all_tiles.append(image.tile[0][3][0])
                image.seek(image.tell()+1)
        except EOFError:
            image.seek(0)

        all_tiles = tuple(set(all_tiles))

        try:
            while 1:
                try:
                    duration = image.info["duration"]
                except:
                    duration = 100

                duration *= .001 #convert to milliseconds!
                cons = False

                if "loop" in image.info:
                  self.loops = (image.info["loop"] == 0)

                x0, y0, x1, y1 = (0, 0) + image.size
                if image.tile:
                    tile = image.tile
                else:
                    image.seek(0)
                    tile = image.tile
                if len(tile) > 0:
                    x0, y0, x1, y1 = tile[0][1]

                if all_tiles:
                    if all_tiles in ((6,), (7,)):
                        cons = True
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    elif all_tiles in ((7, 8), (8, 7)):
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    else:
                        palette = base_palette
                else:
                    palette = base_palette

                pi2 = None
                try:
                  pi = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
                  pi.set_palette(palette)
                  if "transparency" in image.info:
                      pi.set_colorkey(image.info["transparency"])
                  pi2 = pygame.Surface(image.size, SRCALPHA)
                  if cons:
                      for i in self.frames:
                          pi2.blit(i[0], (0,0))
                  pi2.blit(pi, (x0, y0), (x0, y0, x1-x0, y1-y0))
                  if self.flipped:
                    pi2 = pygame.transform.flip(pi2, True, False)
                except Exception as e:
                    #print("Exception", e) # Lets hide this exception 
                    pass

                self.frames.append([pi2, duration])
                image.seek(image.tell()+1)
        except EOFError:
            pass

    def render(self, screen, pos, visible):
        if self.running:
            self.frameTime += 1
            if self.frameTime >= int(round(self.frames[self.cur][1]*FPS)):
                if self.reversed:
                    self.cur -= 1
                    if self.cur < self.startpoint:
                        self.cur = self.breakpoint if self.loops else self.cur+1
                else:
                    self.cur += 1
                    if self.cur > self.breakpoint:
                        self.cur = self.startpoint if self.loops else self.cur-1

                self.frameTime = 0
        if visible and screen is not None:
          screen.blit(self.frames[self.cur][0], pos)

    def seek(self, num):
        self.cur = num
        if self.cur < 0:
            self.cur = 0
        if self.cur >= len(self.frames):
            self.cur = len(self.frames)-1

    def set_bounds(self, start, end):
        if start < 0:
            start = 0
        if start >= len(self.frames):
            start = len(self.frames) - 1
        if end < 0:
            end = 0
        if end >= len(self.frames):
            end = len(self.frames) - 1
        if end < start:
            end = start
        self.startpoint = start
        self.breakpoint = end

    def pause(self):
        self.running = False

    def play(self):
        self.running = True

    def rewind(self):
        self.seek(0)
    def fastforward(self):
        self.seek(self.length()-1)

    def get_height(self):
        return self.image.size[1]
    def get_width(self):
        return self.image.size[0]
    def get_size(self):
        return self.image.size
    def length(self):
        return len(self.frames)
    def reverse(self):
        self.reversed = not self.reversed
    def reset(self):
        self.cur = 0
        self.frameTime = 0
        self.reversed = False

    def copy(self):
        new = GIFImage(self.filename)
        new.running = self.running
        new.breakpoint = self.breakpoint
        new.startpoint = self.startpoint
        new.cur = self.cur
        new.frameTime = self.frameTime
        new.reversed = self.reversed
        return new
