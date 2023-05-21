import os, re
import pickle


def get_classes():
    if os.path.isfile("./geotask/points.pickle"):
        print("Using existing points.pickle")
        with open('./geotask/points.pickle', 'rb') as handle:
            b = pickle.load(handle)
            return b
