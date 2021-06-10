import glob

blocked = ["/etc/passwd", "/flag.txt", "/proc/"]

def read_file(file_path):
    for i in blocked:
        if i in file_path:
                return "you aren't allowed to read that file"
    
    try:
        path = glob.glob(file_path)[0]
    except:
        return "file doesn't exist"
    
    return open(path, "r").read()

user_input = input("> ")
print(read_file(user_input))