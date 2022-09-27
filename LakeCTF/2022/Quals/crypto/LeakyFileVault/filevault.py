#!/usr/local/bin/python3
from hashlib import blake2s
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from binascii import unhexlify
import pathlib

BLOCK_SIZE = 8


def pad(data, block_size):
    if len(data) % block_size == 0:
        return data
    else:
        return data + b'\x00' * (block_size - len(data) % block_size)


def merge(left, right):
    hash = blake2s(left, digest_size=BLOCK_SIZE)
    hash.update(right)
    return hash.digest()


def merkleTree(data, height):
    data = pad(data, BLOCK_SIZE)

    output_size = BLOCK_SIZE * (2**height)
    if len(data) <= output_size:
        raise ValueError(f"Not enough data to create a merkle tree. Need > {output_size} bytes, got {len(data)}")

    # compute recursively the previous layer of the tree
    if len(data) > 2 * output_size:
        data = merkleTree(data, height+1)

    # compute the current layer based on the layer below
    for i in range(len(data)//BLOCK_SIZE - 2**height):
        prefix = data[:i*BLOCK_SIZE]
        left = data[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE]
        right = data[(i+1)*BLOCK_SIZE:(i+2)*BLOCK_SIZE]
        suffix = data[(i+2)*BLOCK_SIZE:]

        data = prefix + merge(left, right) + suffix

    return data


file_index = {'admin': set(), 'guest': set()}


def get_file_path(data):
    global data_folder
    return data_folder / merkleTree(data, 2).hex()


def upload(user, data, file_hash=None):
    """
    Upload a file to the vault.
    A file_hash of height 3 or more can be provided to avoid re-hashing the data.
    """

    if user not in file_index:
        file_index[user] = set()

    if file_hash is None:
        file_hash = merkleTree(data, 3)
    else:
        file_hash = merkleTree(file_hash, 3)

    if all(file_hash not in file_index[user] for user in file_index):
        with open(get_file_path(file_hash), 'wb') as f:
            f.write(data)

    file_index[user].add(file_hash)


def download(user, file_hash):
    """
    Download a file from the vault.
    A user can only download their own files.
    """

    if file_hash not in file_index[user]:
        raise ValueError("File not found")
    with open(get_file_path(file_hash), 'rb') as f:
        return f.read()


def list_files():
    table = Table(title="FileVault™")
    table.add_column("user")
    table.add_column("file hash")

    for user in file_index.keys():
        for file_hash in file_index[user]:
            table.add_row(user, file_hash.hex())

    console.print(table)


data_folder = pathlib.Path("/tmp/filevault")
data_folder.mkdir(exist_ok=True)

with open('flag.png', 'rb') as f:
    data = f.read()
    file_hash = merkleTree(data, 4)
    upload('admin', data, file_hash)
    del data

console = Console(width=140)
console.print("Welcome to FileVault™")

while True:
    try:
        user = "guest"
        cmd = Prompt.ask(
            f"{user}@filevault:", choices=["list", "upload", "download"], default="list")
        match cmd:
            case "list":
                list_files()
            case "upload":
                data = Prompt.ask("data (hex)")
                if len(data)//2 > 8*BLOCK_SIZE:
                    upload(user, unhexlify(data))
                else:
                    console.print(f"To avoid collisions, the data must be more than {8*BLOCK_SIZE} bytes long")
            case "download":
                file_hash = Prompt.ask("file hash (hex)")
                print(download(user, unhexlify(file_hash)).hex())

    except Exception as e:
        console.print_exception(show_locals=True)
