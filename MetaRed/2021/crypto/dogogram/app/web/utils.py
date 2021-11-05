from PIL import Image, ImageChops
from hashlib import md5
from uuid import uuid4
import sqlite3

def compareJPG(file1, file2):
    img1 = Image.open(file1)
    img2 = Image.open(file2)

    equal_size = img1.height == img2.height and img1.width == img2.width

    equal_content = not ImageChops.difference(
        img1.convert("RGB"), img2.convert("RGB")
    ).getbbox()

    return equal_size and equal_content

def whitelistAdd(fd):
    print('wla')
    con = sqlite3.connect("whitelist.db")
    cur = con.cursor()
    fd.stream.seek(0)
    fhash = md5(fd.read()).hexdigest()
    cur.execute("insert into whitelist (hash) values (?)", (fhash,))
    con.commit()

def isWhitelisted(fd):
    print('wl')
    con = sqlite3.connect("whitelist.db")
    cur = con.cursor()
    fd.stream.seek(0)
    fhash = md5(fd.read()).hexdigest()
    cur.execute("select * from whitelist where hash = ?", (fhash,))
    row = cur.fetchone()
    if row is None:
        return False
    else:
        return True

def saveFile(fd):
    fid = str(uuid4())
    fd.stream.seek(0)
    fd.save("static/uploads/" + fid + ".jpg")
    return fid
