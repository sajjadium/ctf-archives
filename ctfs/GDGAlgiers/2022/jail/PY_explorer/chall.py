#!/usr/local/bin/python3


def customDir(obj, expr):
    result = dir(obj)
    print("\n".join(f"{i}] {sub}" for i, sub in enumerate(result)))
    ind = input("index of next object -> ")
    if checkInt(ind) and -len(result) <= int(ind) < len(result):
    	try : 
        	obj, expr = getattr(obj, result[int(ind)]), expr + f".{result[int(ind)]}"
    	except AttributeError: 	
    		print("That attribute doesn't exist")
    else:
        print("Supply a correct index")

    if isinstance(obj, dict):
        print(obj)
        key = input("Enter a key -> ")
        if key in obj.keys():
            return obj[key], expr + f"['{key}']"
        else:
            print("Wrong key")
    return obj, expr


def subclasses(obj, expr):
    try:
        result = obj.__subclasses__()
        print("\n".join(f"{i}] {sub}" for i, sub in enumerate(result)))
        ind = input("index of next object -> ")
        if checkInt(ind) and -len(result) <= int(ind) < len(result):
            return result[int(ind)], expr + f".__subclasses__()[{int(ind)}]"
        else:
            print("Supply a correct index")
    except:
        print("Can't run subclasses on the current object")
    return obj, expr


def checkInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def welcome():
    print("""
Welcome to PY Explorer. I'll give you a tour around my code and let you change what you don't like.
How to use : 
1- Choose any object you want.
1- After finishing and choosing, I will run this : obj1 = obj2
"""
    )


def explore():
    obj = object
    expr = "object"
    finished = False
    while not finished:
        print(
            """0- exit
1- explore dir 
2- check subclasses
3- show current object
4- clear
5- Done
"""
        )
        choice = input("--> ")
        match choice:
            case "0":
                exit()
            case "1":
                obj, expr = customDir(obj, expr)
            case "2":
                obj, expr = subclasses(obj, expr)
            case "3":
                print(obj)
            case "4":
                obj = object
                expr = "object"
            case "5":
                finished = True
    return expr


welcome()
left_expr = explore()
right_expr = explore()

# Time for you to make changes
try:
    exec(f"{left_expr} = {right_expr}")
except:
    print("Impossible to change")

