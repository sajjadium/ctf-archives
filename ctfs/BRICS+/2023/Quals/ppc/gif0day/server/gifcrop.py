import glob
import sys

from PIL import Image, ImageSequence


def crop_image(img: Image) -> Image:
    return img.crop((40, 40, 70, 70))


def crop_gif(gif_path: str):
    with Image.open(gif_path) as im:
        new_frames = ImageSequence.all_frames(im, crop_image)
        duration = new_frames[0].info['duration']
    new_frames[0].save(gif_path, format='GIF',
                       save_all=True, append_images=new_frames[1:], optimize=True, duration=duration, loop=False,
                       append=True)


if __name__ == '__main__':
    p = sys.argv[1]
    for gif_path in glob.glob(p):
        crop_gif(gif_path)
