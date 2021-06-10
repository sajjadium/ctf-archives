from glife import *
import golly as g
import time
import os
import re

vals = []


def add_data(PATTERN_FN):

    g.select([-2753, 891, 1092, 1397])
    g.clear(0)
    g.select([])

    input_str = open(PATTERN_FN,"r").read()

    firstbreak = input_str.find("\n")
    if firstbreak == -1:
        g.show("Error, no newlines found, invalid format")
        g.exit()

    info_line = input_str[0:firstbreak]
    input_str = input_str[firstbreak:]

    #x = 1581, y = 1396, rule = Varlife
    dataptrn = re.compile(br'x = (?P<xval>[0-9]{1,4}), y = (?P<yval>[0-9]{1,4}), rule = .*')

    match = dataptrn.match(info_line)
    xval = 0
    yval = 0

    if (match):
        xval = int(match.group("xval"), 10)
        yval = int(match.group("yval"), 10)

    else:
        g.show("ERROR invalid format {}".format(info_line))
        g.exit()


    ipat = pattern(input_str)
    minbox = getminbox(ipat)

    if max(xval, minbox.x) > 1200:
        g.show("ERROR inserted cell area too wide, max width is 1090")
        g.exit()

    if max(yval, minbox.y) > 1397:
        g.show("ERROR inserted cell area too tall, max height is 1397")
        g.exit()

    startx = -1661-xval
    starty = 891

    #blankptrn.put(startx, starty)

    g.show("width={}, height={} startx={}, starty={}, xval={}, yval={}, bytes={}".format(minbox.wd, minbox.height, startx, starty, xval, yval, len(input_str)))
    ipat.put(startx, starty)
    return "Pattern load data: width={}, height={} startx={}, starty={}, xval={}, yval={}, bytes={}".format(minbox.wd, minbox.height, startx, starty, xval, yval, len(input_str))

attempt_id = os.getenv("GOLLY_ATTEMPT_ID")
if attempt_id is None and os.getenv("LIFEBOX_DEBUG") is not None:
    attempt_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeffffff"

BASE_RESULTS_PATH = os.path.join(os.sep, "tmp", attempt_id)

if not os.path.exists(BASE_RESULTS_PATH):
    os.makedirs(BASE_RESULTS_PATH)

RESULTS_FN = os.path.join(BASE_RESULTS_PATH, "results.log")
open(RESULTS_FN,"a").write("Opening up MC file..\n")

g.open("adventure_lifebooox.mc")
g.setrule('Varlife')
g.show("Starting....")
g.update()
g.setstep(6)
start_time = time.time()

open(RESULTS_FN,"a").write("BOOTING..\n")

PATTERN_FN = os.path.join(BASE_RESULTS_PATH, "pattern.dat")
results = add_data(PATTERN_FN)
open(RESULTS_FN,"a").write(results + "\n")

boot_completed = False

for x in range(0, 40):

    g.run(1000000)

    end_time = time.time() - start_time

    val_last_ins = g.getcell(-1575, 2049)
    val_cutoff = g.getcell(-1618, 1618)
    g.show("Took {} secs state = {}\n".format(end_time, val_last_ins))

    g.update()
    if val_cutoff == 6:
        open(RESULTS_FN, "a+").write("System booted in {}\n".format(end_time, val_last_ins))
        boot_completed = True
        break
    elif val_last_ins == 7:
        open(RESULTS_FN, "a+").write("#{} Bootup signal not sent \n".format(x+1, end_time))
        break
    else:
        open(RESULTS_FN, "a+").write("#{} Bootup taken {} secs so far \n".format(x+1, end_time))

if boot_completed:

    start_time2 = time.time()

    open(RESULTS_FN, "a+").write("Starting Adventure\n")

    for x in range(0, 100):

        g.run(1000000)

        end_time = time.time() - start_time2

        val_last_ins = g.getcell(-62, 1213)

        g.show("#{} Adventure has run for {} secs Total run time {} secs, Adventure game running = {}, \n".format(x+1, end_time, time.time() - start_time, val_last_ins == 6))

        g.update()

        if val_last_ins == 7:
            open(RESULTS_FN, "a+").write("Game finished in {}\n".format(end_time, val_last_ins))
            break
        else:
            key1 = g.getcell(-106, 1543) == 7
            key2 = g.getcell(-106, 1521) == 7
            key3 = g.getcell(-106, 1499) == 7
            open(RESULTS_FN, "a+").write("#{} Adventure has run for {} secs Total run time {} secs, state = {}, Found key1={}, key2={}, key3={}\n".format(x+1, end_time, time.time() - start_time, val_last_ins == 6, key1, key2, key3))

    for x in range(0, 16):
        if g.getcell(-106, 1213 + (x * 22)) == 7:
            vals.append("1")
        else:
            vals.append("0")
else:
    open(RESULTS_FN, "a+").write("LIFEBOX failed to boot within 40m steps.\n")

vals = "".join(vals)

g.show(vals)

if vals == "0000010100111001":
    g.show("WINNER1")
    open(RESULTS_FN, "a+").write("WINNER #1\n".format())
elif vals == "0111101001101001":
    g.show("WINNER2")
    open(RESULTS_FN, "a+").write("WINNER #2\n".format())
else:
    open(RESULTS_FN, "a+").write("GAME OVER\n")

