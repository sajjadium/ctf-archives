# coding: utf-8
import os
import random
import typing as t
from PIL.Image import new as createImage, Image, QUAD, BILINEAR
from PIL.ImageDraw import Draw, ImageDraw
from PIL.ImageFilter import SMOOTH
from PIL.ImageFont import FreeTypeFont, truetype
from io import BytesIO
import time

ColorTuple = t.Union[t.Tuple[int, int, int], t.Tuple[int, int, int, int]]

DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
DEFAULT_FONTS = [os.path.join(DATA_DIR, 'DroidSansMono.ttf')]


class Captcha:
    lookup_table: t.List[int] = [int(i * 1.97) for i in range(256)]

    def __init__(self, width: int = 160, height: int = 60, key: int = None, length: int = 4, 
                 fonts: t.Optional[t.List[str]] = None, font_sizes: t.Optional[t.Tuple[int]] = None):
        self._width = width
        self._height = height
        self._length = length
        self._key = (key or int(time.time())) + random.randint(1,100)
        self._fonts = fonts or DEFAULT_FONTS
        self._font_sizes = font_sizes or (42, 50, 56)
        self._truefonts: t.List[FreeTypeFont] = []
        random.seed(self._key)


    @property
    def truefonts(self) -> t.List[FreeTypeFont]:
        if self._truefonts:
            return self._truefonts
        self._truefonts = [
            truetype(n, s)
            for n in self._fonts
            for s in self._font_sizes
        ]
        return self._truefonts

    @staticmethod
    def create_noise_curve(image: Image, color: ColorTuple) -> Image:
        w, h = image.size
        x1 = random.randint(0, int(w / 5))
        x2 = random.randint(w - int(w / 5), w)
        y1 = random.randint(int(h / 5), h - int(h / 5))
        y2 = random.randint(y1, h - int(h / 5))
        points = [x1, y1, x2, y2]
        end = random.randint(160, 200)
        start = random.randint(0, 20)
        Draw(image).arc(points, start, end, fill=color)
        return image

    @staticmethod
    def create_noise_dots(image: Image, color: ColorTuple, width: int = 3, number: int = 30) -> Image:
        draw = Draw(image)
        w, h = image.size
        while number:
            x1 = random.randint(0, w)
            y1 = random.randint(0, h)
            draw.line(((x1, y1), (x1 - 1, y1 - 1)), fill=color, width=width)
            number -= 1
        return image

    def _draw_character(self, c: str, draw: ImageDraw, color: ColorTuple) -> Image:
        font = random.choice(self.truefonts)

        left, top, right, bottom = draw.textbbox((0, 0), c, font=font)
        w = int((right - left)*1.7) or 1
        h = int((bottom - top)*1.7) or 1

        dx1 = random.randint(0, 4)
        dy1 = random.randint(0, 6)
        im = createImage('RGBA', (w + dx1, h + dy1))
        Draw(im).text((dx1, dy1), c, font=font, fill=color)

        # rotate
        im = im.crop(im.getbbox())
        im = im.rotate(random.uniform(-30, 30), BILINEAR, expand=True)

        # warp
        dx2 = w * random.uniform(0.1, 0.3)
        dy2 = h * random.uniform(0.2, 0.3)
        x1 = int(random.uniform(-dx2, dx2))
        y1 = int(random.uniform(-dy2, dy2))
        x2 = int(random.uniform(-dx2, dx2))
        y2 = int(random.uniform(-dy2, dy2))
        w2 = w + abs(x1) + abs(x2)
        h2 = h + abs(y1) + abs(y2)
        data = (
            x1, y1,
            -x1, h2 - y2,
            w2 + x2, h2 + y2,
            w2 - x2, -y1,
        )
        im = im.resize((w2, h2))
        im = im.transform((w, h), QUAD, data)
        return im

    def create_captcha_image(self, chars: str, color: ColorTuple, background: ColorTuple) -> Image:
        image = createImage('RGB', (self._width, self._height), background)
        draw = Draw(image)

        images: t.List[Image] = []
        for c in chars:
            if random.random() > 0.5:
                images.append(self._draw_character(" ", draw, color))
            images.append(self._draw_character(c, draw, color))

        text_width = sum([im.size[0] for im in images])

        width = max(text_width, self._width)
        image = image.resize((width, self._height))

        average = int(text_width / len(chars))
        rand = int(0.25 * average)
        offset = int(average * 0.1)

        for im in images:
            w, h = im.size
            mask = im.convert('L').point(self.lookup_table)
            image.paste(im, (offset, int((self._height - h) / 2)), mask)
            offset = offset + w + random.randint(-rand, 0)

        if width > self._width:
            image = image.resize((self._width, self._height))

        return image

    def generate_image(self, chars: str) -> Image:
        background = random_color(238, 255)
        color = random_color(10, 200, random.randint(220, 255))
        im = self.create_captcha_image(chars, color, background)
        self.create_noise_dots(im, color)
        self.create_noise_curve(im, color)
        im = im.filter(SMOOTH)
        return im

    def generate(self, format: str = 'png') -> (BytesIO,str):
        code = generate_code(self._length)
        im = self.generate_image(code)
        out = BytesIO()
        im.save(out, format=format)
        out.seek(0)
        return out, code

    def write(self, output: str, format: str = 'png') -> (Image, str):
        code = generate_code(self._length)
        im = self.generate_image(code)
        im.save(output, format=format)
        return im, code


def random_color(start: int, end: int, opacity: t.Optional[int] = None) -> ColorTuple:
    red = random.randint(start, end)
    green = random.randint(start, end)
    blue = random.randint(start, end)
    if opacity is None:
        return (red, green, blue)
    return (red, green, blue, opacity)

def generate_code(length: int = 4):
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(characters) for _ in range(length))