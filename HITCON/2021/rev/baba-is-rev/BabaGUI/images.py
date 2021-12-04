# Original code from https://github.com/nicksandau/GIFImage_ext/blob/master/GIFImage_ext.py

from PIL import Image
import pygame
from pygame.locals import SRCALPHA
import time


class GIFImage(object):
    def __init__(self, filename):
        self.filename = filename
        self.image = Image.open(filename)
        self.original_size = self.image.size
#Added by NS  *********************
        #self.frames = []
        self.fps_scale = 1
        self.img_scale = 1
#**********************************
        self.get_frames()

        self.cur = 0
        self.ptime = time.time()

        self.running = True
        self.breakpoint = len(self.frames)-1
        self.startpoint = 0
        self.reversed = False

    def get_rect(self):
        return pygame.rect.Rect((0, 0), self.image.size)

    def get_frames(self):
        image = self.image
        #Added by NS  ************
        self.frames = []
        #*************************
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
                except Exception as e:
                    print("Error '{0}' occurred. Arguments {1}.",
                          e.message, e.args)
                    duration = 100

                duration *= .001  # convert to milliseconds!

                #Added by NS  ************
                duration *= self.fps_scale
                #*************************

                cons = False

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

                pi = pygame.image.fromstring(
                    image.tobytes(), image.size, image.mode)
                pi.set_palette(palette)
                if "transparency" in image.info:
                    pi.set_colorkey(image.info["transparency"])
                pi2 = pygame.Surface(image.size, SRCALPHA)
                if cons:
                    for i in self.frames:
                        pi2.blit(i[0], (0, 0))
                pi2.blit(pi, (x0, y0), (x0, y0, x1-x0, y1-y0))

                self.frames.append([pi2, duration])
                image.seek(image.tell()+1)
        except EOFError:
            pass

    def render(self, screen, pos):
        if self.running:
            if time.time() - self.ptime > self.frames[self.cur][1]:
                if self.reversed:
                    self.cur -= 1
                    if self.cur < self.startpoint:
                        self.cur = self.breakpoint
                else:
                    self.cur += 1
                    if self.cur > self.breakpoint:
                        self.cur = self.startpoint

                self.ptime = time.time()
        #Added by NS  **************************************
        if self.img_scale == 1:
            surf = self.frames[self.cur][0]
        else:
            surf = pygame.transform.scale(self.frames[self.cur][0],
                                          (int(self.image.width * self.img_scale),
                                           int(self.image.height * self.img_scale)))
        screen.blit(surf, pos)
        #screen.blit(self.frames[self.cur][0], pos)
        #***************************************************

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

#added by NS  ********************************
    def next_frame(self):
        if self.running:
            self.pause()
        else:
            self.cur += 1
            if self.cur > self.breakpoint:
                self.cur = self.startpoint

    def prev_frame(self):
        if self.running:
            self.pause()
        else:
            self.cur -= 1
            if self.cur < 0:
                self.cur = self.breakpoint

    def slow_down(self):
        self.fps_scale += .05 if self.fps_scale != .01 else .04
        self.get_frames()
        self.seek(self.cur)

    def speed_up(self):
        if self.fps_scale - .05 <= 0:
            self.fps_scale = .01
        else:
            self.fps_scale -= .25
        self.get_frames()
        self.seek(self.cur)

    def scale(self, scale_factor):
        self.img_scale += scale_factor

    def reset_scale(self):
        self.img_scale = 1
#*********************************************

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
        self.ptime = time.time()
        self.reversed = False

    def copy(self):
        new = GIFImage(self.filename)
        new.running = self.running
        new.breakpoint = self.breakpoint
        new.startpoint = self.startpoint
        new.cur = self.cur
        new.ptime = self.ptime
        new.reversed = self.reversed
        #Added by NS  ****
        new.fps_scale = self.fps_scale
        #*****************
        return new
