from flask import Flask, request, render_template, abort, make_response

import subprocess
import string
import random
import os
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

colors = [ "#61f2ff", "#f25e95", "#fffb96", "#b03bbf", "#5234bf", "#f24534" ]

command_text_add = r"""convert -size 840x{height} -geometry +0+300 -gravity center -background none -stroke white -strokewidth 1 -fill white -font /var/www/flyer/static/Beon-Regular.ttf -pointsize 36 -interline-spacing 20 -kerning 1.5 label:"{text}" \( +clone   -background "{color}"   -shadow 100x2+0+0 \) +swap \( +clone   -background "{color}"   -shadow 100x5+0+0 \) +swap \( +clone   -background "{color}"   -shadow 100x11+0+0 \) +swap \( +clone   -background "{color}"   -shadow 100x19+0+0 \) +swap -background none -layers merge /var/www/flyer/assets/flyer.png +swap -gravity center -composite {tmpfile} > /dev/null 2>&1"""
charWidth = {',': 9.5, '-': 14.5, '0': 28.5, '1': 15.5, '2': 19.5, '3': 21.5, '4': 20.5, '5': 22.5, '6': 22.5, '7': 18.5, '8': 21.5, '9': 22.5, 'A': 24.5, 'B': 24.5, 'C': 28.5, 'D': 26.5, 'E': 23.5, 'F': 22.5, 'G': 28.5, 'H': 25.5, 'I': 9.5, 'J': 21.5, 'K': 23.5, 'L': 22.5, 'M': 33.5, 'N': 25.5, 'O': 30.5, 'P': 22.5, 'Q': 30.5, 'R': 23.5, 'S': 22.5, 'T': 23.5, 'U': 26.5, 'V': 25.5, 'W': 35.5, 'X': 29.5, 'Y': 26.5, 'Z': 26.5, '_': 17.5, 'a': 21.5, 'b': 23.5, 'c': 22.5, 'd': 23.5, 'e': 23.5, 'f': 18.5, 'g': 23.5, 'h': 24.5, 'i': 8.5, 'j': 8.5, 'k': 20.5, 'l': 8.5, 'm': 39.5, 'n': 24.5, 'o': 23.5, 'p': 23.5, 'q': 23.5, 'r': 20.5, 's': 21.5, 't': 19.5, 'u': 24.5, 'v': 23.5, 'w': 32.5, 'x': 23.5, 'y': 24.5, 'z': 22.5, ' ': 12.5}

@app.route('/')
def index():
    return render_template("base.html")

@app.route('/generate', methods=['POST'])
def generate():
    color = request.form.get("color", None)
    text = request.form.get("text", None)
    if not color or not text:
        abort(400, "Missing arguments")
    if int(color) not in range(6):
        abort(400, "Invalid color")
    if len(text) > 438:
        abort(400, "Text too large")
    return create_flyer(text, int(color))

def create_flyer(text, color):
    global command_text_add
    global colors
    color = colors[color]

    tmpfile = "/tmp/" + random_string(16) + ".png"
    (height, text) = cutstring(text)

    cmd = command_text_add.format(
        height = height,
        text = text,
        color = color,
        tmpfile = tmpfile
    )
    subprocess.run(cmd.encode('utf-8'), shell=True, timeout=10, cwd="/var/www/flyer")
    if not os.path.isfile(tmpfile):
        abort(500, "Error creating flyer")
    with open(tmpfile, "rb") as f:
        imgdata = f.read()
    resp = make_response(imgdata)
    os.remove(tmpfile)
    resp.headers['Content-Type'] = 'image/png'
    resp.headers['Content-Disposition'] = 'attachment;filename=flyer.png'
    return resp

def random_string(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def filterString(x):
    forbidden_chars = '"#$%\'()*+/:;<=>?@[\\]^`{|}~'
    if x in forbidden_chars:
        abort(403, f"Found illegal string {x}")

def cutstring(s):
  global charWidth
  try:
    s = s.strip()
    lengthWord = 0
    lengthLine = 0
    sLine = ''
    sWord = ''
    wordLength = 0
    countList = 0
    sPrint = ''
    for char in s:
      filterString(char)
      if char in charWidth.keys():
        lengthWord = lengthWord + (charWidth[char])
        lengthLine = lengthLine + (charWidth[char])
      else:
        lengthWord = lengthWord + 25
        lengthLine = lengthLine + 25
      if lengthLine < 800:
        if char != ' ':
          sWord = (str(sWord) + str(char))
        else:
          sLine = (str(sLine) + str(sWord))
          lengthWord = 0
          sWord = char
      elif lengthWord > 800:
          abort(400, f"Word {sWord} too long to fit on a line")
      else:
        sPrint = (str(sPrint) + str(((str(sLine) + str('DeL1m3T3r!')))))
        lengthLine = 0
        for i in sWord:
          if i in charWidth.keys():
            filterString(i)
            lengthWord = lengthWord + (charWidth[char])
            lengthLine = lengthLine + (charWidth[char])
          else:
            lengthWord = lengthWord + 25
            lengthLine = lengthLine + 25
        sLine = ''
        sWord = (str(sWord) + str(char))
    if char != ' ':
      sLine = (str(sLine) + str(sWord))
      sPrint = (str(sPrint) + str(sLine))
    sPrintList = sPrint.split('DeL1m3T3r!')
    textHeight = len(sPrintList) * 60
    if textHeight > 780:
        abort(400, "Height too long: " + str(textHeight))
    text = '\\n'.join(sPrintList)
    if len(text) > 460:
        abort(400, "Length too long: " + str(len(text)))
    return(textHeight,text)
  except Exception as error:
      if isinstance(error, HTTPException):
          abort(error.code, error.description)
      return(780, s)
