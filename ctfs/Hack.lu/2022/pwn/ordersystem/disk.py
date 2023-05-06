'''
This file provides functions for dumping from memory to disk,
useful for persistence.
'''
from os import path

ROOT = path.normpath(path.join(path.abspath(__file__),'..'))

def _store(fname,content):
    full = path.join(ROOT,fname)

    open(full,'w').write(content.hex())
    
def store_disk(entries):
    for k,v in entries.items():
        try:
            k = k.decode()
        except:
            k = k.hex()

        storagefile = path.normpath(f'storage/{k}')
        _store(storagefile,v)
