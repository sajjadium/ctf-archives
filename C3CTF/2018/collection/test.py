import Collection

a = Collection.Collection({"a":1337, "b":[1.2], "c":{"a":45545}})

print(a.get("a"))
print(a.get("b"))
print(a.get("c"))


