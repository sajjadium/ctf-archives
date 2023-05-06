from ctypes import c_ulong

def read(where):
  return c_ulong.from_address(where).value

def write(what, where):
  c_ulong.from_address(where).value = what

menu = '''|| PYWRITE ||
1: read
2: write
> '''

while True:
  choice = int(input(menu))
  if choice == 1:
    where = int(input("where? "))
    print(read(where))
  if choice == 2:
    what = int(input("what? "))
    where = int(input("where? "))
    write(what, where)
  if choice == 3:
    what = input("what????? ")
    a = open(what)
    print(a)
