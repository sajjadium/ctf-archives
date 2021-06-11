#/usr/bin/env python3
import json
import os.path
import secrets
import subprocess
import sys
import signal
import tempfile


def die(*args, **kwargs):
    print("ERROR:", *args, "Goodbye!", **kwargs)
    exit(1)


def fix_stupid_python_stuff_and_set_up_alarm():
    # Why don't you default to utf8 if there is no LOCALE, python?
    sys.stdout.flush()
    sys.stdout = open(sys.stdout.buffer.fileno(), 'w', 1, encoding='utf8')
    sys.stderr.flush()
    sys.stderr = open(sys.stderr.buffer.fileno(), 'w', 1, encoding='utf8')
    # Why can't you simply shut up about SIGPIPE, python?
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    signal.signal(signal.SIGALRM, lambda *a: die("Your time is up!"))
    signal.alarm(10)


def format_number_list(numbers):
    fmt = ", ".join(["%d"] * (len(numbers)-1) + ["and %d"])
    return fmt % tuple(sorted(numbers))


def read_solutions(config):
    nums = format_number_list(config["flags"])
    print("Hello! Send me a json array of [key, val, arg] lists and I will")
    print("execute `key=val bash script.sh arg' for each of them. You get")
    print("a flag when you have %s solutions with unique keys." % nums)
    print("You may need to shutdown the input (send eof, -N in nc).\n")
    try:
        solutions = json.load(sys.stdin)
    except json.decoder.JSONDecodeError:
            die("Not a json.");
    if not isinstance(solutions, list):
        die("The json is not an array.")
    if not all(isinstance(e, list) for e in solutions):
        die("Some elements of the json array are not lists.");
    if not all(len(row) == 3 for row in solutions):
        die("Some rows of the json array are too short/long.")
    if not all(isinstance(e, str) for row in solutions for e in row):
        die("Some elements of the rows of the json array are not strings.")    
    return solutions


def check(flag, key, val, arg):
    try:
        ff = tempfile.NamedTemporaryFile("wt", encoding="utf-8")
        ff.file.write(flag)
        ff.file.flush()

        env = {key: val}
        cmd = [
            "nsjail",
            "--mode", "o",
            "--time_limit", "5",
            "--keep_env",
            "-u", "1000",
            "-g", "1000",
            "-T", "/dev",
            "-R", "/bin",
            "-R", "/lib",
            "-R", "/lib64",
            "-R", "/usr",
            "-R", "/sbin",
            "-R", "{}:/issues.txt".format(os.path.abspath("./issues.txt")),
            "-R", "{}:/flag".format(os.path.abspath(ff.name)),
            "-R", "{}:/script.sh".format(os.path.abspath("./script.sh")),
            "--",
            "/bin/bash", "/script.sh", arg,
        ]
        pipe = subprocess.PIPE
        sub = subprocess.Popen(cmd, env=env, stdout=pipe, stderr=pipe)
        out, err = sub.communicate()
        return flag.encode() in out or flag.encode() in err
    except KeyboardInterrupt:
        raise
    except:
        return False
    finally:
        ff.close()


def read_config():
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)
    config["flags"] = {int(k): v for k, v in config["flags"].items()}
    return config


if __name__ == "__main__":
    fix_stupid_python_stuff_and_set_up_alarm()
    
    config = read_config()
    solutions = read_solutions(config)

    seen = set()
    good = 0
    for i, (key, val, arg) in enumerate(solutions):
        if key in seen:
            print(i, "FAILURE, already used this key:", repr(key))
            continue
        seen.add(key)

        flag = "FlagFragment{%s}" % secrets.token_hex(32)
        if check(flag, key, val, arg):
            good += 1
            print(i, "success, key was", repr(key))
        else:
            print(i, "FAILURE, key was", repr(key))

    print("\nOverall, you got", good, "right, so you...")

    for limit, flag in sorted(config["flags"].items()):
        if good >= limit:
            print("  ...get a flag for", limit, "unique solutions:", flag)

    if good > max(config["flags"]):
        print("  ...get a flag for being too good at exploiting:", config["unintended"])

    if good < min(config["flags"]):
        print("  ...get nothing. Try harder!")
