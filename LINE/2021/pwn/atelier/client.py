#!/usr/bin/env python3

import sys
import json
import asyncio
import importlib

# from sqlalchemy import *

class AtelierException:
    def __init__(self, e):
        self.message = repr(e)

class MaterialRequest:
    pass

class MaterialRequestReply:
    pass

class RecipeCreateRequest:
    def __init__(self, materials):
        self.materials = materials

class RecipeCreateReply:
    pass

def object_to_dict(c):
    res = {}
    res["__class__"] = str(c.__class__.__name__)
    res["__module__"] = str(c.__module__)
    res.update(c.__dict__)
    return res

def dict_to_object(d):
    if "__class__" in d:
        class_name = d.pop("__class__")
        module_name = d.pop("__module__")
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)

        inst = class_.__new__(class_)
        inst.__dict__.update(d)
    else:
        inst = d

    return inst

async def rpc_client(message):
    message = json.dumps(message, default=object_to_dict)

    reader, writer = await asyncio.open_connection(sys.argv[1], int(sys.argv[2]))
    writer.write(message.encode())
    data = await reader.read(2000)
    writer.close()

    res = json.loads(data, object_hook=dict_to_object)
    if isinstance(res, AtelierException):
        print("Exception: " + res.message)
        exit(1)

    return res

print("""
         ,✿   ✿      ✿
        / |  -|- ,-✿ |  ✿ ,-✿ ,-✿
✿'`✿'  /--|   |  |-' |  | |-' |   ✿'`✿'
     ,'   `-' `' `-' `' ' `-' '

     Author: twitter.com/vsnrain

Hi and welcome to my Atelier!
I am making a handy database to store my alchemy recipes.
I have not finished adding all of the recipes yet, but you can try crafting some of them if you want.
""")
loop = asyncio.get_event_loop()

req = MaterialRequest()
res = loop.run_until_complete(rpc_client(req))

print("\nMaterial 1:")
for i, m in enumerate(res.material1):
    print(f"{i}: {m}")
input1 = int(input("Choose material 1: "))
material1 = res.material1[input1]

print("\nMaterial 2:")
for i, m in enumerate(res.material2):
    print(f"{i}: {m}")
input2 = int(input("Choose material 2: "))
material2 = res.material2[input2]

req = RecipeCreateRequest(f"{material1},{material2}")
res = loop.run_until_complete(rpc_client(req))

print("\nResult :\n" + res.result)

loop.close()
