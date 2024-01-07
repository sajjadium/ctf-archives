from flask import Flask, request, send_file, render_template
import json
from PIL import Image
from io import BytesIO
import numpy as np

app = Flask(__name__)

MOKERS = {
        "flag": {"description": "Free Flag (whatever)", "private": False, "preview": "%5B%7B%22filter%22%3A+%22blur%22%2C+%22args%22%3A+%5B20%5D%7D%5D"},
        "moker1": {"description": "Moker: normal", "private": False, "preview": "[]"},
        "moker2": {"description": "Moker (very different)", "private": False, "preview": "%5B%7B%22filter%22%3A+%22warp%22%2C+%22args%22%3A+%5B%5B%5B-1%2C+0%2C+768%5D%2C+%5B0%2C+-1%2C+1024%5D%2C+%5B0%2C+0%2C+1%5D%5D%5D%7D%5D"},
        "moker3": {"description": "Moker (holy)", "private": False, "preview": "%5B%7B%22filter%22%3A+%22intensity%22%2C+%22args%22%3A+%5B%5B0%2C+1%5D%2C+%5B0%2C+0.6%5D%5D%7D%2C+%7B%22filter%22%3A+%22gamma%22%2C+%22args%22%3A+%5B0.2%5D%7D%5D"},
        "moker4": {"description": "Moker... but at what cost?", "private": False, "preview": "%5B%7B%22filter%22%3A+%22rotate%22%2C+%22args%22%3A+%5B77%5D%7D%2C+%7B%22filter%22%3A+%22resize%22%2C+%22args%22%3A+%5B%5B768%2C+1024%5D%5D%7D%5D"},
        "moker5": {"description": "[FRESH] Moker", "private": False, "preview": "%5B%7B%22filter%22%3A+%22swirl%22%2C+%22args%22%3A+%5Bnull%2C+3%2C+500%5D%7D%5D"},
        "flagmoker": {"description": "Moker with Special Flag (RARE, do not show!)", "private": True, "preview": "[]"},
}

for moker in MOKERS:
    MOKERS[moker]["blob"] = Image.open("images/" + moker + ".png")

########### HELPERS

@app.after_request
def csp(r):
    # Actually, it's not even an XSS challenge.
    r.headers["Content-Security-Policy"] = "default-src 'none'; style-src 'self' https://cdn.jsdelivr.net; img-src 'self'; script-src https://cdn.jsdelivr.net;"
    return r

from skimage.filters import gaussian as blur
from skimage.exposure import adjust_gamma as gamma, rescale_intensity as intensity
from skimage.transform import resize, rotate, swirl, warp

FILTERS = {
        "blur": blur,
        "gamma": gamma,
        "intensity": lambda i, a, b: intensity(i, tuple(a), tuple(b)),
        "resize": resize,
        "rotate": rotate,
        "swirl": swirl,
        "warp": lambda i, m: warp(i, np.array(m))
}

import time
def doFilterChain(image, chain):
    for f in chain:
        image = FILTERS[f["filter"]](image, *f["args"])

    return image

########### ROUTES

@app.route("/")
def home():
    return render_template("index.html", MOKERS=MOKERS)

@app.route("/style.css")
def style():
    return send_file("style.css")

@app.route("/view/<moker>", methods=["GET"])
def view(moker):
    if moker not in MOKERS:
        return "What?"

    moker = MOKERS[moker]

    image = moker["blob"]

    filters = request.args.get("filters", None)
    if filters is not None:
        filters = json.loads(filters)
        image = np.array(image) / 255
        image = doFilterChain(image, filters)
        image = Image.fromarray((image * 255).astype(np.uint8), 'RGB')

    if moker["private"]:
        return "Not for public consumption."

    io = BytesIO()
    image.save(io, "PNG")
    io.seek(0)
    return send_file(io, mimetype='image/png')
