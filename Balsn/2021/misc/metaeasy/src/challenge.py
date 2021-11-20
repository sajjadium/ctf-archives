class MasterMetaClass(type):   
    def __new__(cls, class_name, class_parents, class_attr):
        def getFlag(self):
            print('Here you go, my master')
            with open('flag') as f:
                print(f.read())
        class_attr[getFlag.__name__] = getFlag
        attrs = ((name, value) for name, value in class_attr.items() if not name.startswith('__'))
        class_attr = dict(('IWant'+name.upper()+'Plz', value) for name, value in attrs)
        newclass = super().__new__(cls, class_name, class_parents, class_attr)
        return newclass
    def __init__(*argv):
        print('Bad guy! No Flag !!')
        raise 'Illegal'

class BalsnMetaClass(type):
    def getFlag(self):
        print('You\'re not Master! No Flag !!')

    def __new__(cls, class_name, class_parents, class_attr):
        newclass = super().__new__(cls, class_name, class_parents, class_attr)
        setattr(newclass, cls.getFlag.__name__, cls.getFlag)
        return newclass

def secure_vars(s):
    attrs = {name:value for name, value in vars(s).items() if not name.startswith('__')}
    return attrs

safe_dict = {
            'BalsnMetaClass' : BalsnMetaClass,
            'MasterMetaClass' : MasterMetaClass,
            'False' : False,
            'True' : True,
            'abs' : abs,
            'all' : all,
            'any' : any,
            'ascii' : ascii,
            'bin' : bin,
            'bool' : bool,
            'bytearray' : bytearray,
            'bytes' : bytes,
            'chr' : chr,
            'complex' : complex,
            'dict' : dict,
            'dir' : dir,
            'divmod' : divmod,
            'enumerate' : enumerate,
            'filter' : filter,
            'float' : float,
            'format' : format,
            'hash' : hash,
            'help' : help,
            'hex' : hex,
            'id' : id,
            'int' : int,
            'iter' : iter,
            'len' : len,
            'list' : list,
            'map' : map,
            'max' : max,
            'min' : min,
            'next' : next,
            'oct' : oct,
            'ord' : ord,
            'pow' : pow,
            'print' : print,
            'range' : range,
            'reversed' : reversed,
            'round' : round,
            'set' : set,
            'slice' : slice,
            'sorted' : sorted,
            'str' : str,
            'sum' : sum,
            'tuple' : tuple,
            'type' : type,
            'vars' : secure_vars,
            'zip' : zip,
            '__builtins__':None
            }

def createMethod(code):
    if len(code) > 45:
        print('Too long!! Bad Guy!!')
        return
    for x in ' _$#@~':
        code = code.replace(x,'')
    def wrapper(self):
        exec(code, safe_dict, {'self' : self})
    return wrapper

def setName(pattern):
    while True:
        name = input(f'Give me your {pattern} name :')
        if (name.isalpha()):
            break
        else:
            print('Illegal Name...')
    return name

def setAttribute(cls):
    attrName = setName('attribute')
    while True:
        attrValue = input(f'Give me your value:')
        if (attrValue.isalnum()):
            break
        else:    
            print('Illegal value...')
    setattr(cls, attrName, attrValue)

def setMethod(cls):
    methodName = setName('method')
    code = input(f'Give me your function:')       
    func = createMethod(code)
    setattr(cls, methodName, func)

def getAttribute(obj):
    attrs = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]
    x = input('Please enter the attribute\'s name :')
    if x not in attrs:
        print(f'You can\'t access the attribute {x}')
        return
    else:
        try:
            print(f'{x}: {getattr(obj, x)}')
        except:
            print("Something went wrong in your attribute...")
            return
    
def callMethod(cls, obj):
    attrs = [attr for attr in dir(obj) if callable(getattr(obj, attr)) and not attr.startswith("__")]
    x = input('Please enter the method\'s name :')
    if x not in attrs:
        print(f'You can\'t access the method {x}')
        return
    else:
        try:
            print(f'calling method {x}...')
            cls.__dict__[x](obj)
            print('done')
        except:
            print('Something went wrong in your method...')
            return

class Guest(metaclass = BalsnMetaClass):
    pass

if __name__ == '__main__':
    print(f'Welcome!!We have prepared a class named "Guest" for you')
    cnt = 0
    while cnt < 3:
        cnt += 1
        print('1. Add attribute')
        print('2. Add method')
        print('3. Finish')
        x = input("Option ? :")
        if x == "1":
            setAttribute(Guest)
        elif x == "2":
            setMethod(Guest)
        elif x == "3":
            break
        else:
            print("invalid input.")
            cnt -= 1
    print("Well Done! We Create an instance for you !")
    obj = Guest()
    cnt = 0
    while cnt < 3:
        cnt += 1
        print('1. Inspect attribute')
        print('2. Using method')
        print('3. Exit')
        x = input("Option ? :")
        if x == "1":
            getAttribute(obj)
        elif x == "2":
            callMethod(Guest, obj)
        elif x == "3":
            print("Okay...exit...")
            break
        else:
            print("invalid input.")
            cnt -= 1
