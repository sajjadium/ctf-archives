#!/usr/bin/env python
import os
import base64
import tempfile
import subprocess

SOURCE_FILE = "Main.java"
DEP_FILE = "dep.jar"


def get_file(filename: str):
    print(f"Please send me the file {filename}.")
    content = input("Content: (base64 encoded)")
    data = base64.b64decode(content)
    if len(data) > 1024 * 1024:
        raise ValueError("Too long")
    with open(filename, "wb") as fp:
        fp.write(data)


def main():
    print("Welcome to the secured Java sandbox.")
    with tempfile.TemporaryDirectory() as dir:
        os.chdir(dir)
        get_file("Main.java")
        get_file("dep.jar")
        print("Compiling...")
        try:
            subprocess.run(
                ["javac", "-cp", DEP_FILE, SOURCE_FILE],
                input=b"",
                check=True,
            )
        except subprocess.CalledProcessError:
            print("Failed to compile!")
            exit(1)

        print("Running...")
        try:
            subprocess.run(["java", "--version"])
            subprocess.run(
                [
                    "java",
                    "-cp",
                    f".:{DEP_FILE}",
                    "-Djava.security.manager",
                    "-Djava.security.policy==/dev/null",
                    "Main",
                ],
                check=True,
            )
        except subprocess.CalledProcessError:
            print("Failed to run!")
            exit(2)


if __name__ == "__main__":
    main()
