#!/usr/bin/env python3

# https://pypi.org/project/console/
from console.screen import Screen
from console.utils import wait_key
from console import fg

from multiprocessing import Process, Manager
from typing import List
from dataclasses import dataclass
import re

@dataclass
class File:
    name: str
    contents: str
    owner: str

@dataclass
class User:
    name: str
    disallowed_commands: List[str]

cwd = "/home/a/"
user_input = ''
user_input_store = ''

history = []
history_idx = 0
            
users = {
    "alice": User("alice", ["cat"]),
    "bob": User("bob", ["cat"]),
    "eve": User("eve", []),
}

files = {
    cwd+"flag.txt": File("flag.txt", open("flag.txt").read(), "alice"),
    cwd+"bobthoughts.bob": File("bobthoughts.bob", open("bobthoughts.bob").read(), "bob"),
    cwd+"fl@g.txt": File("fl@g.txt", open("fl@g.txt").read(), "eve"),
}

class Command: 
    valid_commands = {
        "login": "Login as a user.\r\n\tUsage: login <username>",
        "cat": "Display file contents (absolute paths only).\r\n\tUsage: cat <filename>",
        "ls": "List files in the current directory.\r\n\tUsage: ls",
        "whoami": "Display current users.\r\n\tUsage: whoami",
        "pwd": "Print working directory.\r\n\tUsage: pwd",
        "help": "Display this help text.\r\n\tUsage: help",
    }

    def __init__(self, cmd):
        self.cmd = cmd

    def start(self):
        global g
        Process(target=self.run, args=tuple()).start()

    def run(self):
        global screen_buffer, users, current_user
        
        if self.cmd.strip() == '':
            screen_buffer += list('\r\n>>> ')
            return

        cmd_vals = self.cmd.strip().split()
        cmd = cmd_vals[0]
        args = cmd_vals[1:]
        
        if cmd in users[current_user.value].disallowed_commands:
            screen_buffer += fmt(f"{self.cmd}\r\nUser {current_user.value} does not have permission to run {cmd}.\r\n")
        elif cmd not in self.valid_commands:
            screen_buffer += fmt(f"{self.cmd}\r\nInvalid command '{cmd}'.\r\n")
        else:
            screen_buffer += fmt(self.cmd + "\r\n")
            func = getattr(self, f"_{cmd}")
            screen_buffer += fmt(func(*args))
            
        screen_buffer += list(">>> ")

    def _login(self, *args):
        global current_user
        if len(args) == 0:
            return "Must provide user to login as.\r\n"
        if args[0] in users:
            current_user.value = args[0]
            return f"Logged in as {current_user.value}\r\n"
        return "That user doesn't exist!\r\n"

    def _cat(self, *args):
        global files, current_user
        if len(args) == 0:
            return "No file provided.\r\n"
        fname = args[0]
        if fname[0][0] != '/':
            return "Absolute paths only.\r\n"
        if fname not in files:
            return "File not found.\r\n"
        if files[fname].owner != current_user.value:
            return f"User {current_user.value} does not have permission to read file {fname}.\r\n"
        return files[fname].contents

    def _ls(self, *args):
        global files
        ret = "Filename\t\t\t\tOwner\r\n"
        ret += '-'*48 + "\r\n"
        for fname in files:
            ret += fname + "\t\t\t" + files[fname].owner + '\r\n'
        return ret

    def _help(self, *args):
        global current_user, users
        ret = ''
        for cmd in self.valid_commands:
            if cmd in users[current_user.value].disallowed_commands:
                continue
            ret += cmd + ":\t" + self.valid_commands[cmd] + "\r\n\r\n"
        return ret[:-1]

    def _whoami(self, *args):
        global current_user
        return current_user.value + "\r\n"

    def _pwd(self, *args):
        global cwd
        return cwd + "\r\n"

def p(*args, **kwargs):
    global screen
    print(*args, **kwargs)
    screen._stream.flush()

# quick hack to make colors work on remote
# comment this class out if running locally

class fg:
    yellow = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    red = '\033[31m'
    lightgreen = '\033[92m'
    lightmagenta = '\033[95m'
    default = '\033[37m'

def fmt(s):
    highlights = {
        r"((?<=\W)\d+(?=\W))": fg.yellow,
        r"((['\"]).*?\2)": fg.blue,
        "(" + '|'.join(i for i in Command.valid_commands) + ')': fg.cyan,
        r"((/.+)+\.[a-z]{3})": fg.lightmagenta,
        r"((?<=\W)(" + '|'.join(i for i in users) + r')(?<=\W))': fg.purple,
        r"(ictf{.*?})": fg.lightgreen,
        r"(jctf{.*?})": fg.red,
    }

    for rx in highlights:
        s = re.sub(rx, highlights[rx] + r"\1" + fg.default, s)
    return list(s)

def clr():
    global screen
    p(screen.clear, end='')
    p(screen.move_to(0, 0), end='')

def read_key():
    key = wait_key()
    if key == '\x1b':
        for _ in range(2):
            key += wait_key()
    return key

def handle_key():
    global user_input, history, history_idx, user_input_store
    key = read_key()
    match key:
        case "\x03":
            exit() # Ctrl+C
        case "\x04":
            exit() # Ctrl+D
        case "\x7f":
            if len(user_input) > 0:
                user_input = user_input[:-1]
        case "\r" | "\n" | "\r\n":
            Command(user_input).start()
            if len(user_input.strip()) > 0:
                history.append(user_input)
            history_idx = 0
            user_input_store = ""
            user_input = ""
        case '\x1b[A': # up
            history_idx += 1
            if history_idx > len(history):
                history_idx = len(history)
            user_input = [user_input_store, *history][-history_idx]
        case '\x1b[B': # down
            history_idx -= 1
            if history_idx < 0:
                history_idx = 0
            user_input = [user_input_store, *history][-history_idx]
        # I wish I had the time to implement right/left arrow keys
        case '\x1b[C': # right
            ...
        case '\x1b[D': # left
            ...
        case _:
            user_input += key
            user_input_store = user_input

def main():
    global screen, screen_buffer, user_input
    with screen.fullscreen():
        screen_buffer += list(">>> ")
        p(">>> ", end='')
        while 1:
            handle_key()
            text = ''.join(screen_buffer)
            clr()
            p(text, end='')
            p(user_input, end='')

if __name__ == '__main__':
    with Screen(force=True) as screen:
        with Manager() as g:
            screen_buffer = g.list([])
            current_user = g.Value(str, "alice")

            main()
