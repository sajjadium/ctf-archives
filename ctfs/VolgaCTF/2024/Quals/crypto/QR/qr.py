from PIL import Image
from secret import flag
from lfsr_parameters import register, branches
import qrcode


QR_FILE = 'qr_flag.png'


class LFSR:
    def __init__(self, register, branches):
        self.register = register
        self.branches = branches
        self.n = len(register)

    def next_bit(self):
        ret = self.register[self.n - 1]
        new = 0
        for i in self.branches:
            new ^= self.register[i - 1]
        self.register = [new] + self.register[:-1]

        return ret


def qr_text(text: bytes):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=0,
    )
    qr.add_data(text.decode())
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')

    img.save(QR_FILE)


def encrypt_png(png_path: str, result_path: str):
    generator = LFSR(register, branches)

    image = Image.open(png_path)
    w = image.width
    h = image.height

    new_image = Image.new(image.mode, image.size)
    pixels = image.load()

    for y in range(h):
        for x in range(w):
            pixel = pixels[x, y] // 255
            next_bit = generator.next_bit()
            encrypted = pixel ^ next_bit

            new_image.putpixel((x, y), encrypted * 255)

    new_image.save(result_path, image.format)


if __name__ == '__main__':
    qr_text(flag)
    encrypt_png(QR_FILE, 'qr.png')
