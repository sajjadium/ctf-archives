import pyvirtualdisplay.smartdisplay
import easyprocess
import shutil
import time
import sys
import os

GOLLY_BINARY = "/usr/games/golly /lifebox-run.py"
DEBUG = 0

def start(attempt_id, results_log):
    last_len = 0
    same_cnt = 0
    with pyvirtualdisplay.smartdisplay.SmartDisplay(visible=False, size=(1300, 900)) as v_display:
        if DEBUG:
            print (v_display)
            print (v_display.display)

        env = os.environ
        env["GOLLY_ATTEMPT_ID"] = attempt_id
        env["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        env["TERM"] = "xterm"
        env["PWD"] = "/"
        env["HOME"] = "/home/rrx"

        print(env["GOLLY_ATTEMPT_ID"])
        sys.stdout.flush()

        open(results_log, "a").write("Starting up lifebooox\n")

        with easyprocess.EasyProcess(GOLLY_BINARY, env=env) as golly:

            for x in range(0, 500):

                results = open(results_log).read()

                if results.find("WINNER") > -1:
                    break
                if results.find("GAME OVER") > -1:
                    break
                if results.find("#100") > -1:
                    golly.sendstop()
                    break
                if last_len == len(results):

                    same_cnt += 1
                else:
                    same_cnt = 0

                # if the process has not logged anything new for 120 secs then kill it.
                if same_cnt > 10:
                    with open(results_log, "a") as log:
                        log.write("The game of life went too long without update, check the format of the uploaded pattern.\n")
                        log.write("GAME OVER\n")
                    golly.sendstop()
                    break
                last_len = len(results)

                time.sleep(3)

def main():
    start("9ffd9372-2d04-4afa-954e-30c9c370317f","/tmp/9ffd9372-2d04-4afa-954e-30c9c370317f/results.log")

if __name__ == '__main__':
    main()