import sys

def main():
  if len(sys.argv) != 2:
    print("Invalid args")
    return

  password = sys.argv[1]
  builder = 0
  
  for c in password:
    builder += ord(c)
  
  if builder == 713 and len(password) == 8 and (ord(password[2]) == ord(password[5])):
    if (ord(password[3]) == ord(password[4])) and ((ord(password[6])) == ord(password[7])):
        print("correct")
    else:
        print("incorrect")
  else:
    print("incorrect")

if __name__ == "__main__":
  main()