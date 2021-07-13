import os
import sys
import uuid
import shutil
import string 

# Gets the file from the user
def get_file():
    # Get the size of the file
    print "Size: ",
    size = int(raw_input())

    if(size > 1000000):
        print "File too big" 
        sys.exit(0) 

    print "File Contents\n"
    print "================="

    file_contents = sys.stdin.read(size)
    return file_contents

# Write a file
def write_file(name, contents):
    fd = open(name, "w+")
    fd.write(contents)
    fd.close()

    # Specify the permissions of the file
    os.chown(name, 0, 0) # Root user
    os.chmod(name, 0o777) # Read & execute

# Clean up the current execution
def cleanup(foldername):
    shutil.rmtree(foldername)

# Setup process information for a user making a call
def setup_call():

    filename = str(uuid.uuid4())
    foldername = str(uuid.uuid4())
    folder = "/home/ctf/programs/"

    # Get the file from the user
    contents = get_file()

    # Location of the chroot jail
    os.mkdir(folder + foldername)
    os.mkdir(folder + foldername + "/etc")

    # Copy the standard user information here
    shutil.copy("/etc/passwd", folder + foldername + "/etc/passwd") 

    # Move the current working directory in here for later
    os.chdir(folder + foldername)

    # User executable to create
    write_file(folder + foldername + "/" + filename, contents)

    # No special characters, spaces and (most importantly) "."s 
    allowlist = set(string.ascii_lowercase + string.digits + "/" + "-")
    filename = ''.join(c for c in filename if c in allowlist)

    command = "/home/ctf/MaxDebugger " + "./" + filename 
    os.system(command)
    cleanup(folder + foldername) 

setup_call()

