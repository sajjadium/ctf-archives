#builder.py

#UMDCTF Challenge: i_see_many_paths
#Developed on Python 3.12.0 (tags/v3.12.0:0fb18b0, Oct  2 2023, 13:03:39) [MSC v.1935 64 bit (AMD64)] on win32

import string
import random
import hashlib
import py7zr
import os

#===========================================================
#Constants
#===========================================================

with open("flag.txt", 'r') as f:
    FLAG = f.read()
    
MIN_CHILDREN = 1
MAX_CHILDREN = 4

MAX_DEPTH = 10
random.seed("My name is Paul Muad'dib Atreides, duke of arrakis".encode()) #!!!

#===========================================================
#Functions
#===========================================================

COUNT = 0
def get_new_int():
    global COUNT
    COUNT = COUNT + 1
    return COUNT

def random_string(length):
    # Create a random string of the specified length
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_encrypted_zip(output_filename, files, password):
    #Create a 7z file with the given list of files, encrypted with a password. Each of the files zipped are then removed to save space.
    with py7zr.SevenZipFile(output_filename, 'w', password=password) as archive:
        for file in files:
            archive.write(file.filename, arcname=os.path.basename(file.filename))
            os.remove(file.filename)

class ZipNode():
    def __init__(self, filename, children):
        self.filename = filename
        self.children = children
        self.password = hashlib.md5(filename.encode()).hexdigest()

    def __str__(self):
        return "Name: {}".format(self.filename)

def generate_random_tree(root, depth):
    if (depth >= MAX_DEPTH):
        return

    if (depth >= MAX_DEPTH * (3 / 4)):
        root.children.append(ZipNode("possible_flag_{}.txt".format(get_new_int()), []))

    for i in range(MIN_CHILDREN, random.randint(MIN_CHILDREN, MAX_CHILDREN) + 1):
        child = ZipNode("future_number_{}.7z".format(get_new_int()), [])

        root.children.append(child)

        generate_random_tree(child, depth + 1)

def tree_to_zip_file(root):
    for child in root.children:
        if (child.filename[-3:] == "txt"):
            open(child.filename, 'w+').write(FLAG if (random.random() < 0.0005) else random_string(random.randint(5, 35)))
        else:
            tree_to_zip_file(child)

    create_encrypted_zip(root.filename, root.children, root.password)
        

#===========================================================
#Entry Point
#===========================================================

root = ZipNode("root.7z", [])

generate_random_tree(root, 0)
tree_to_zip_file(root)




    
