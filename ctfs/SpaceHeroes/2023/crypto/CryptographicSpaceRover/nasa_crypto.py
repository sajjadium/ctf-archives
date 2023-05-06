import psutil
import datetime
import os
import signal
import subprocess
import uuid
import setproctitle

#python3 -m pip install setproctitle

def get_dashes(perc):
    dashes = "|" * int((float(perc) / 10 * 4))
    empty_dashes = " " * (40 - len(dashes))
    return dashes, empty_dashes

def print_top(guess, uuid):
    cat_check = 0
    if(guess == True):
        setproctitle.setproctitle(str(uuid))
        setproctitle.setthreadtitle(str(uuid))

    print(f"top - {str(datetime.timedelta(seconds=psutil.boot_time()))}")
    percs = psutil.cpu_percent(interval=0, percpu=True)
    for cpu_num, perc in enumerate(percs):
        dashes, empty_dashes = get_dashes(perc)
        line = " CPU%-2s [%s%s] %5s%%" % (cpu_num, dashes, empty_dashes, perc)
        print(line)

    virtual_memory = psutil.virtual_memory()
    print(f"MiB Swap :\t{virtual_memory.total / 1024 / 1024:.2f} total\t{virtual_memory.free / 1024 / 1024:.2f} free\t{virtual_memory.used / 1024 / 1024:.2f} used\t{virtual_memory.active / 1024 / 1024:.2f} active")
    swap_memory = psutil.swap_memory()
    print(f"MiB Swap :\t{swap_memory.total / 1024 / 1024:.2f} total\t{swap_memory.free / 1024 / 1024:.2f} free\t{swap_memory.used / 1024 / 1024:.2f} used")

    listOfProcessNames = []
    for proc in psutil.process_iter():
        pInfoDict = proc.as_dict(attrs=['pid', 'username', 'cpu_percent', 'memory_percent', 'status', 'name']) # Get process detail as dictionary
        listOfProcessNames.append(pInfoDict) # Add to list

    print(f'{"PID":>6}{"USER":>10}{"%CPU":>6}{"%MEM":>6}{"STATUS":>15}{"NAME":>45}')
    for elem in listOfProcessNames:
        print(f'{elem["pid"]:>6}{elem["username"]:>10}{elem["cpu_percent"]:>6}{elem["memory_percent"]:>6.2f}{elem["status"]:>15}{elem["name"]:>45}')

    if (guess == True):
        setproctitle.setproctitle("python3")
        setproctitle.setthreadtitle("python3")


def logo(uuid):
    ascii_art = """
             ____________________________________________________
            /                                                    \\
           |    _____________________________________________     |
           |   |                                             |    |
           |   |  Welcome to the NASA Lunar Rover.           |    |
           |   |                                             |    |
           |   |  Session UUID:                              |    |
           |   |    {0}     |    |
           |   |                                             |    |
           |   |  This program should help us track CPU      |    |
           |   |      usage but it seems to spawn extra      |    |
           |   |      processes when we give it certain      |    |
           |   |      characters.                            |    |
           |   |                                             |    |
           |   |  Can you help us narrow down what           |    |
           |   |      characters to avoid at each index?     |    |
           |   |                                             |    |
           |   |  Enter your characters below.               |    |
           |   |  Thanks, The Space Heroes                   |    |
           |   |_____________________________________________|    |
           |                                                      |
            \_____________________________________________________/
                   \_______________________________________/
    """.format(uuid)
    print(ascii_art)

def main():
    session_uuid = uuid.uuid4()
    flag = open('flag.txt', 'r').readline().strip('\n').lower()

    logo(session_uuid)
    print("Please enter characters:: ")

    user_guess = input().lower().strip("\n")

    for i in range(0, len(flag)):
        if i+1 > len(user_guess):
            print_top(guess=None, uuid=session_uuid)
            exit(-1)
        elif (user_guess[i] != flag[i]):
            print_top(guess=False, uuid=session_uuid)
        else:
            print_top(guess=True,uuid=session_uuid)

    if user_guess == flag:
        print(f"Thanks; we'll avoid these characters: {flag}")

if __name__ == "__main__":
    main()
