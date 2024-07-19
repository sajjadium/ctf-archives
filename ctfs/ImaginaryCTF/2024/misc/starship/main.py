#!/usr/bin/env python3

import pandas as pd
from io import StringIO
from sklearn.neighbors import KNeighborsClassifier
from gen import gen_data

done = False
flag = open("flag.txt").read().strip()

def menu():
  print("1. show dataset")
  print("2. train model")
  print("3. predict state")
  print("4. check incoming objects")

def train_dataset(dataset):
  df = pd.read_csv(StringIO(dataset))
  X, y = df.iloc[:, :-1].values, df.iloc[:, -1].values
  model = KNeighborsClassifier(n_neighbors=3)
  model.fit(X, y)
  return model

if __name__ == "__main__":
  print("<[ missle defense system control panel ]>")
  menu()

  print("initializing...")
  while True:
    dataset, incoming = gen_data()
    model = train_dataset(dataset)
    pred1 = model.predict([list(map(int, incoming[0].split(",")))])
    pred2 = model.predict([list(map(int, incoming[1].split(",")))])
    if pred1[0] == "enemy" and pred2[0] == "enemy":
      break

  while True:
    choice = int(input("> "))
    if choice == 1:
      print("--- BEGIN DATASET ---")
      print(dataset)
      print("--- END DATASET ---")
    if choice == 2:
      model = train_dataset(dataset)
      print("model trained!")
    if choice == 3:
      inp = input("enter data: ")
      pred = model.predict([list(map(int, inp.split(",")))])
      print(f"result: {pred}")
    if choice == 4:
      pred1 = model.predict([list(map(int, incoming[0].split(",")))])
      pred2 = model.predict([list(map(int, incoming[1].split(",")))])
      print(f"target 1: {incoming[0]} | result: {pred1[0]}")
      print(f"target 2: {incoming[1]} | result: {pred2[0]}")
      if pred1[0] == "friendly" and pred2[0] == "friendly":
        print(f"flag: {flag}")
    if choice == 42 and not done:
      inp = input("enter data: ")
      inp = inp.split(",")
      for i in range(9):
        inp[i] = int(inp[i])
      if len(inp) == 10:
        dataset = dataset.strip() + "\n" + ",".join(map(str,inp))
        done = True
