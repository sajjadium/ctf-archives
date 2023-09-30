import os
from socket import socket
import socketserver
import select
import subprocess

NIXOWOS = r"""
                         _______              ____________           _______
                        /       \             \           \         /       \
                       \         \              \          \       /         \
                        \          \             \          \    /           /
                         \          \              \         \  /          /               __
                           \         \              \         \/          /          _____/ /
           __               \         \               \                 /    _____---      /
           \ -----____       \         ---------------\\               /___--             /
            \         ---\     \                       \ \           /_/                 /
             \            \____/                         \\         \                    /
              \               ____________________________\\         \                  /
               \            _----------/                     \        \                /
                \          /          /                       \        \              /
                 \       /          /                           \       \  _________/
                   \    /           >>>>                     <<<<\       \/-------
   __________________\/          /      >>>               <<<      \     //       \_______________
  /                             /       >>>               <<<       \  //                         \
 /                            /     >>>>                     <<<<    \//                           \
 \                           //\            ww         ww            /                             /
  \_____________           / /  \   ><><>< ww    www    ww ><><><   /          ___________________/
               /          //      \         wwwwww wwwwww          /          /
              /          //        \                             /           /
            /          / \           \                          /          /
           /          /    \          \                       /           /
          \          /      \          \   __________________/___________/_________________
           \       /          \          \ \                                             /
             \    /            \          \ \                                           /
              \  /            /            \ \                                         /
               \/            /               \\_______________          ______________/
                            /                 \               \         \
                          /         ___        \               \         \
                         /         /   \         \              \          \
                        /         /     \         \               \         \
                       \         /        \        \               \         /
                        \       /          \        \               \       /
                         -------            ----------               -------"""

class ReuseAddr(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    allow_reuse_port = True

class Server(socketserver.StreamRequestHandler):
    request: socket
    def handle(self):
        def say(m):
            if isinstance(m, str):
                m = (m + '\n').encode('utf-8')
            self.request.sendall(m)
        def get():
            return self.request.recv(4096)

        say(NIXOWOS)
        say("Welcome to Maple Bacon's Flakey CI\n\n")

        say('Enter a git-https repo URL to build, e.g. github.com/lf-/flaketest')
        repo = get().decode('utf-8').strip()
        print('repo: ', repo)

        if 'nixpkgs' in repo:
            say("Please don't clone nixpkgs, it will take a very long time and cause problems")
            self.request.close()
            return

        say('Enter a flake output to build, e.g. packages.x86_64-linux.default:')
        output = get().decode('utf-8').strip()
        print('flake output', output)

        cmd = ['nix', 'build', '-v', '--accept-flake-config', '--print-build-logs', '--print-out-paths', '--refresh', f'git+https://{repo}#{output}']
        say('$ ' + ' '.join(cmd))
        print(cmd)

        proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pollobj = select.poll()
        if proc.stderr is None or proc.stdout is None:
            # wtf
            raise ValueError('stdout or stderr is none wtf')
        pollobj.register(proc.stderr.fileno())
        pollobj.register(proc.stdout.fileno())
        go = 2
        while go > 0:
            fds = pollobj.poll(1.)
            for (fd, ev) in fds:
                if ev == select.POLLIN:
                    data = os.read(fd, 2048)
                    self.request.sendall(data)
                    print(data)
            if go == 1:
                go = 0
            elif proc.poll() is not None:
                go = 1
        say('done')
        print('done')
        self.request.close()


if __name__ == '__main__':
    svc = ReuseAddr(('0.0.0.0', 1337), Server)
    svc.allow_reuse_address = True
    svc.allow_reuse_port = True
    svc.serve_forever()
