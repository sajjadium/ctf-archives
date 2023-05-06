import fitz
import base64
import tempfile
import os
import json

inputtext = input("Give me a text: ")[:1024]
uspassword = input("Choose a user password for your document: ")
owpassword = input("Choose a owner password for your document: ")
options_inp = input("Options for Document.save(): ")

allow_options = [
    "garbage", "clean", "deflate", "deflate_images", "deflate_fonts", 
    "incremental", "ascii", "expand", "linear", "pretty", 
    "no_new_id", "permissions"
]

try:
    options_load = json.loads(options_inp)
    options = {}
    for opt in options_load:
        if opt in allow_options:
            options[opt] = options_load[opt]
            break
except:
    options = {}

try:
    tempfd, temppath = tempfile.mkstemp(prefix="eaas_")
    os.close(tempfd)
except:
    print("Create temp file failed. Please contact with admin.")
    exit(-1)

try:
    pdf = fitz.Document()
    pdf.new_page()
    pdf[0].insert_text((20,30), inputtext, fontsize=14, color=(0,0,0))
    pdf.save(temppath, owner_pw=owpassword, user_pw=uspassword, encryption=fitz.PDF_ENCRYPT_AES_128, **options)
except:
    print("Create the secret document failed. Try again.")
    exit(0)

try:
    with open(temppath, "rb") as f:
        print(base64.b64encode(f.read()).decode())
except:
    print("Couldn't show the file for you. Try again.")
    exit(0)

