import os
from PIL import Image, ImageDraw, ImageFont
import sys

font = ImageFont.truetype('static/generator/comic-sans.ttf', size=48)

outfile = sys.argv[1]
text = sys.argv[2]

if len(text) > 1000: # Too much text :lemonthink:
  text = "Too long!"

width, height = 512, 562
img = Image.new('RGB', (width, height), color=(255, 255, 255))
canvas = ImageDraw.Draw(img)
chunks = []

chunk = ""
for char in text:
  chunk += char
  text_width, text_height = canvas.textsize(chunk, font=font)
  if text_width >= (width-20):
    chunks.append(chunk[:-1])
    chunk = char

if len(chunks) == 0:
  chunks.append(chunk)

if chunks[-1] != chunk:
  chunks.append(chunk)
  
for i,chunk in enumerate(chunks):
  text_width, text_height = canvas.textsize(chunk, font=font)
  x_pos = int((width - text_width) / 2) + 10
  y_pos = 15 + i * 100
  canvas.text((x_pos, y_pos), chunk, font=font, fill='#000000')


if "rarctf" in text: # Don't try and exfiltrate flags from here :lemonthink:
  img = Image.open("static/generator/noleek.png") 
  img.save(f"static/images/{outfile}")
else:
  img2 = Image.open('static/generator/lemonthink.png')
  img.paste(img2, (0, 0), img2.convert('RGBA'))
  if len(chunks) > 1:
    img3 = Image.open("static/generator/move.png").convert('RGBA')
    img3.paste(img, (170,42), img.convert('RGBA'))
    img3.save(f"static/images/{outfile}")
  else:
    img.save(f"static/images/{outfile}")
