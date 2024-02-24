#!/usr/bin/env python3

import os
import signal
import subprocess
import sys
import time
from random import randint

def PoW(l=25):
    x = randint(2**(l-1), 2**l)
    g = randint(2**16, 2**18)
    p = 13066599629066242837866432762953247484957727495367990531898423457215621371972536879396943780920715025663601432044420507847680185816504728360166754093930541
    target = pow(g, x, p)
    print(f"+----------------------- POW -----------------------+")
    print(f"{g}^x mod {p} == {target}")
    print(f"+----------------------- POW -----------------------+")
    try:
        solution = int(input("x: "))
        if solution == x:
            return True
        else:
            return False
    except:
        return False
    
if (PoW() == False):
    exit()

def sigterm_handler(_signo, _stack_frame):
    os.system("kill -9 `pgrep qemu`")
    os.system("kill -9 `pgrep adb`")
    os.system("kill -9 `pgrep emulator`") 
    sys.exit(0)
signal.signal(signal.SIGTERM, sigterm_handler)


adb_port = 11000
emu_port = 11001
home = "/home/user"
apk_path = "/chall/app.apk"

ENV = {}
output = ["This website is the top one I have seen soo far", "This is just meh!!", "I would say quit your passion for web dev"]

def set_ENV(env):
    env.update(os.environ)
    env.update({
        "ANDROID_ADB_SERVER_PORT" : f"{adb_port}",
        "ANDROID_SERIAL": f"emulator-{emu_port}",
        "ANDROID_SDK_ROOT": "/opt/android/sdk",
        "ANDROID_SDK_HOME": home,
        "ANDROID_PREFS_ROOT": home,
        "ANDROID_EMULATOR_HOME": f"{home}/.android",
        "ANDROID_AVD_HOME": f"{home}/.android/avd",
        "JAVA_HOME": "/usr/lib/jvm/java-17-openjdk-amd64",
        "PATH": "/opt/android/sdk/cmdline-tools/latest/bin:/opt/android/sdk/emulator:/opt/android/sdk/platform-tools:/bin:/usr/bin:" + os.environ.get("PATH", "")
    })

def set_EMULATOR():
    subprocess.call(
        "avdmanager" +
        " create avd" +
        " --name 'Pixel_4_XL'" +
        " --abi 'default/x86_64'" +
        " --package 'system-images;android-30;default;x86_64'" +
        " --device pixel_4_xl" +
        " --force"+
        " > /dev/null 2> /dev/null",
        env=ENV,close_fds=True,shell=True)

    return subprocess.Popen(
        "emulator" +
        " -avd Pixel_4_XL" +
        " -no-cache" +
        " -no-snapstorage" +
        " -no-snapshot-save" +
        " -no-snapshot-load" +
        " -no-audio" +
        " -no-window" +
        " -no-snapshot" +
        " -no-boot-anim" +
        " -wipe-data" +
        " -accel on" +
        " -netdelay none" +
        " -netspeed full" +
        " -delay-adb" +
        " -port {}".format(emu_port)+
        " > /dev/null 2> /dev/null ",
        env=ENV,close_fds=True,shell=True)

def ADB_Helper(args,var1=True):
    return subprocess.run("adb {}".format(" ".join(args)),env=ENV,shell=True,close_fds=True,capture_output=var1).stdout

def install_apk():
    ADB_Helper(["install","-r",apk_path])

def start_activity():
    ADB_Helper(["shell","am","start","-n","bi0sctf.android.challenge/.MainActivity"])

def start_broadcast(action,extras=None):
    ADB_Helper(["shell", "am", "broadcast", "-a", action, '--es', 'url',extras['url']])

def print_adb_logs():
     logs = ADB_Helper(["logcat", "-d"])
     for log in logs.decode("utf-8").strip().split("\n"):
         print(log)

def push_file():
    ADB_Helper(["root"])
    ADB_Helper(["push", "/chall/flag", "/data/data/bi0sctf.android.challenge/"])
    ADB_Helper(["unroot"])

def print_prompt(message):
    print(message)
    sys.stdout.flush()


try:
    set_ENV(ENV)
    print_prompt("+-------------------=============-------------------+")
    print_prompt("+------------------ Website Rater ------------------+")
    print_prompt("+-------------------=============-------------------+")
    print_prompt("[+] Waking up the bot for testing your website...")
    emulator = set_EMULATOR()
    #print_adb_logs()
    ADB_Helper(["wait-for-device"])

    print_prompt("[+] Stats: Rated 100 websites today.")
    install_apk()

    print_prompt("[+] Status: Starting the analysing engine.")
    start_activity()
    push_file()

    time.sleep(5)

    print_prompt("[+] Enter your Website: ")
    input_url = sys.stdin.readline().strip()
    start_broadcast("bi0sctf.android.DATA", extras = {"url": input_url})

    reply = output[randint(0, 2)]
    print_prompt("[+] Opinion: " + reply)

    time.sleep(10)

    os.system("kill -9 `pgrep qemu`")
    emulator.kill()
except:
    print("nice try kid")
    os.system("kill -9 `pgrep qemu`")
    os.system("kill -9 `pgrep adb`")
    emulator.kill()

