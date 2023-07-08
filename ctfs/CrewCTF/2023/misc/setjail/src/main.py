import re
import ast

import void

"""
Example:

( when root object is A )
path: .B.C["D"][1][2][3]
value: "pyjail is fun!"

->

A.B.C["D"][1][2][3] = "pyjail is fun!"

"""

DISALLOWED_WORDS = ["os", "posix"]
ROOT_OBJECT = void

def abort(s):
	print(s)
	exit(1)

def to_value(s):
	return ast.literal_eval(s)

# gift
module = input("import: ")
__import__(module)

path = input("path: ")
value = to_value(input("value: "))

path, _, last_item_key, last_attr_key = re.match(r"(.*)(\[(.*)\]|\.(.*))", path).groups()

# set root object
current_obj = ROOT_OBJECT

# walk object
while path != "":
	_, item_key, attr_key, path = re.match(r"(\[(.*?)\]|\.([^\.\[]*))(.*)", path).groups()
	
	if item_key is not None:
		item_key = to_value(item_key)
		if any([word in item_key for word in DISALLOWED_WORDS]):
			abort("deny")
		current_obj = current_obj[item_key]
	elif attr_key is not None:
		if any([word in attr_key for word in DISALLOWED_WORDS]):
			abort("deny")
		current_obj = getattr(current_obj, attr_key)
	else:
		abort("invalid")


# set value
if last_item_key is not None:
	last_item_key = to_value(last_item_key)
	current_obj[last_item_key] = value
elif last_attr_key is not None:
	setattr(current_obj, last_attr_key, value)

print("Done")
