#!/usr/bin/env python3

print("Loading data... Can take 1-2 minutes")

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import numpy as np
import random
import pandas as pd
import json
from secret import FLAG

with open("other_dataset_dga.txt", 'r') as file:
    content = file.read()

dga_domains = content.split("\n")

with open("other_dataset_legit.txt", 'r') as file:
    content = file.read()

legit_domains = content.split("\n")

df = pd.DataFrame()
df['domain'] = random.sample(dga_domains, 5000)
df['dga'] = 1

df_ = pd.DataFrame()
df_['domain'] = random.sample(legit_domains, 5000)
df_['dga'] = 0

df = pd.concat([df, df_], axis=0)
df.reset_index(drop=True, inplace=True)

df = df.reindex(np.random.permutation(df.index))

count = 0

for i in range(0,10000,100):
    print("Here is a new batch of domains : ")
    print(f"{{ 'domains' : {list(df.iloc[i:i+100]['domain'])} }}")
    
    result = input("Enter your analysis - Respect this format : { \"labels\" : [1,0,0,1...] } - With 1 for dga and 0 for legit : ").strip()

    try:
        labels = json.loads(result)["labels"]
    except json.decoder.JSONDecodeError:
        print("Format error !!")
        exit()

    for j in range(i,i+100):
        try :
            if labels[j%100] == df.iloc[j]['dga']:
                count += 1
        except IndexError:
            print("List index out of range")
            exit()

if count > 8500:
    print(f"You're a very good analyst. Here is your flag : {FLAG}")
else:
    print(f"You blocked too many legit domains or didn't block enough malicious domains. Here is your count {count} Try again !")
