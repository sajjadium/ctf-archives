import random

from PIL import Image, ImageDraw, ImageFont

BG_COLOR = (255, 255, 255)
fonts = (
    'JetBrainsMono-Regular.ttf',
    'OpenSans.ttf',
    'Roboto-Regular.ttf'
)

FONT = ImageFont.truetype('/fonts/JetBrainsMono-Regular.ttf', size=100)


def load_font():
    size = random.randint(95, 115)
    return ImageFont.truetype('/fonts/' + random.choice(fonts), size=size)


def random_font_color():
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    if r + g + b > 200 * 3:
        return random_font_color()
    return (r, g, b)


def generate_gif_images(s: str) -> list[Image]:
    frames = []
    for letter in s:
        fnt = load_font()
        image = Image.new("RGB", (200, 200), BG_COLOR)
        draw = ImageDraw.Draw(image)

        for _ in range(500):
            rx, ry = random.randint(0, 199), random.randint(0, 199)
            image.putpixel((rx, ry), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        draw.text((0, 0), letter, font=fnt, fill=random_font_color())
        frames.append(image)
    return frames


def generate_gif(s: str, op):
    images = generate_gif_images(s)
    images[0].save(op, format='GIF', save_all=True, append_images=images[1:], optimize=True, duration=400, loop=False)


if __name__ == '__main__':
    generate_gif('test12', 'test.gif')
