import os
import zipfile
import subprocess
import hmac, hashlib

key = os.environ["KEY"]


def cleanup(filename):
    os.system(f"rm -rf ./files/{filename}.zip")
    os.system(f"rm -rf ./files/{filename}")


def verify_zip(filename):
    try:
        s = open(f"./files/{filename}.zip", "rb").read(4)
        if s != b"PK\x03\x04":
            raise Exception("Invalid zip file (PK header missing)")
    except:
        raise Exception("Unable to read zip file")

    archive = zipfile.ZipFile(f"./files/{filename}.zip", "r")
    try:
        FILES = archive.read("FILES").decode()
        SIGNATURE = archive.read("SIGNATURE").decode()
    except:
        raise Exception("Invalid zip file (FILES or SIGNATURE missing)")

    my_signature = hmac.new(key.encode(), FILES.encode(), hashlib.sha256).hexdigest()
    if my_signature != SIGNATURE:
        raise Exception("Invalid signature (FILES and SIGNATURE mismatch)")


def extract_zip(filename):
    try:
        subprocess.check_call(
            f"7z x ./files/{filename}.zip -o./files/{filename}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
    except:
        raise Exception("Unable to extract")

    try:
        fs = open(f"./files/{filename}/FILES", "r").readlines()
    except:
        raise Exception("Unable to read FILES")

    files = {}
    for l in fs:
        if l == "":
            continue
        parts = l.split(" ", 1)
        files[parts[1].strip()] = parts[0]

    d = os.listdir(f"./files/{filename}")
    if len(d) > 5:
        raise Exception("Too many files")

    for file in d:
        if file == "FILES" or file == "SIGNATURE":
            continue
        if file == ".." or file == ".":
            raise Exception("Invalid file name " + file)

        stat = os.stat(f"./files/{filename}/{file}")
        if stat.st_size > 60 * 1024:
            raise Exception("File too big " + file)

        hash = hashlib.sha256(
            open(f"./files/{filename}/{file}", "rb").read()
        ).hexdigest()
        if file not in files or hash != files[file]:
            raise Exception("Missing file hash for " + file)


def get_flag(filename):
    try:
        f = open(f"./files/{filename}/GET_FLAG", "r").read()
    except:
        raise Exception("Unable to read GET_FLAG")

    if f == "I_WANT_THE_FLAG_PLS":
        return os.environ["FLAG"]
    raise Exception("No flag for you :(")


# !PLEASE DO NOT UPLOAD A ZIP BOMB!
def compute(filename):
    try:
        verify_zip(filename)
        extract_zip(filename)
        flag = get_flag(filename)
        cleanup(filename)
        return flag
    except Exception as e:
        cleanup(filename)
        return str(e)


if __name__ == "__main__":
    import shutil, sys

    file = sys.argv[1]
    filename_without_path = file.split("/")[-1].split(".")[0]
    shutil.copyfile(file, f"./files/{filename_without_path}.zip")
    print(compute(filename_without_path))
