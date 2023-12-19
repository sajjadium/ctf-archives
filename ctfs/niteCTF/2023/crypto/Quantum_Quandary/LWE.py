from secret_value import message
import numpy as np
import json
from pathlib import Path
flag = "nite{xxxxxxxxxxxxxx}"
l = len(message)

def message_to_vector(message):
    vector = [ord(char) for char in message]
    return vector

m = message_to_vector(message)
def randomized_matrix(lower_bound, upper_bound, row, column):
    rando = np.random.uniform(lower_bound, upper_bound, size=(row, column))
    return rando

def randomised_matrix(lower_bound, upper_bound, row, column):
    rando = np.random.randint(lower_bound, upper_bound, size=(row, column))
    return rando

A = randomized_matrix(20, 50, l, l)
s = randomized_matrix(20, 50, l, l)
e = randomised_matrix(-2, 2, l, 1)

t = np.dot(A, s) + e
from numpy import ndarray


def create_cipher(key1, key2, message):
    e1 = randomised_matrix(-2, 2, l, 1)
    e2 = randomised_matrix(-2, 2, l, 1)
    e3 = randomised_matrix(-2, 2, l, 1)

    u = np.dot(key2, e1) + message
    v = np.dot(key1, e1)

    return u, v

u, v = create_cipher(A, t, m)

print(f"u = {ndarray.tolist(u)}")
print(f"v = {ndarray.tolist(v)}")


def dump_values(s, A, t):
    if isinstance(s, np.ndarray):
        dump = {'secret_key': s.tolist(), 'A': A.tolist(), 't': t.tolist()}
    else:
        dump = {'secret_key': s}

    home_directory = Path.home()

    if home_directory:
        dump_folder = home_directory / 'dump'

        if not dump_folder.is_dir():
            try:
                dump_folder.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Error creating dump folder: {e}")
                return

        dump_file = dump_folder / 'dump_values.json'
        try:
            with open(dump_file, 'w') as file:
                json.dump(dump, file, indent=2)
        except Exception as e:
            print(f"Error dumping values to file: {e}")

    else:
        pass

dump_values(s, A, t)