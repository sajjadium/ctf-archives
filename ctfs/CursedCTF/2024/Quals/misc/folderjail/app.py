#!/usr/local/bin/python

import os
import shutil
import tarfile
from folders.folders import FolderAnalyzer, FolderTranspiler

TMP_DIR = '/tmp/program'
def unzip_tar_gz(hex_input):
    tar_gz_data = bytes.fromhex(hex_input)

    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR, exist_ok=True)

    with open(TMP_DIR + '/archive.tar.gz', 'wb') as f:
        f.write(tar_gz_data)

    with tarfile.open(TMP_DIR + '/archive.tar.gz', 'r:gz', dereference=False) as tar:
        tar.extractall(TMP_DIR)

    os.remove(TMP_DIR + '/archive.tar.gz')

hex_input = input("> ")
unzip_tar_gz(hex_input)

tokens = FolderAnalyzer(TMP_DIR).lex()
code = FolderTranspiler(tokens).transpile()

exec(code)