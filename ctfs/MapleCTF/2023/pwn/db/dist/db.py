import sys
from struct import pack, unpack
from subprocess import PIPE, Popen
from threading import Thread
from collections import defaultdict

DB_TIMEOUT = 5.0

class DbException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class Db:
    def __init__(self, db_file):
        self.db_file = db_file
        self.proc = None
        self.rows = None
        self.exception = None
        self.done = False
        self.open()

    def __enter__(self):
        return self

    def __exit__(self, ty, val, tb):
        self.proc.stdin.close()
        self.proc.wait(timeout=1)
        self.proc.terminate()

    def open(self):
        if self.proc is not None and self.proc.poll() is not None:
            self.proc.kill()
        self.proc = Popen(['./db', self.db_file], stdin=PIPE, stdout=PIPE)

    def execute(self, cmd):
        try:
            self.proc.stdin.write(pack('H', len(cmd)) + cmd)
            self.proc.stdin.flush()
        except BrokenPipeError:
            print('reopening database')
            self.open()
            return self.execute(cmd)
        self.rows = []
        self.exception = None
        self.done = False
        t = Thread(target=self.read_rows_timeout)
        t.start()
        t.join(DB_TIMEOUT)
        if self.exception is not None:
            raise self.exception
        return self.rows

    def read_rows_timeout(self):
        try:
            for row in self.read_rows():
                self.rows.append(row)
            self.done = True
        except DbException as e:
            self.exception = e

    def read_resp(self):
        ty = self.proc.stdout.read(1)
        match ty:
            case b'':
                return None
            case b'D':
                return self.read_row()
            case b'X':
                l, = unpack('H', self.proc.stdout.read(2))
                return DbException(self.proc.stdout.read(l))
            case b'I':
                l, = unpack('H', self.proc.stdout.read(2))
                data = self.proc.stdout.read(l)
                return [b'db returned info:', data, len(self.rows)]
            case b'E':
                return None
            case _:
                return [b'db returned other:', ty, len(self.rows)]

    def read_rows(self):
        e = None
        while (r := self.read_resp()) is not None:
            if isinstance(r, Exception):
                e = r
            elif isinstance(r, bytes):
                yield r.decode('latin1')
            else:
                yield r
        if e is not None:
            raise e

    def read_row(self):
        data = []
        cols = self.proc.stdout.read(1)[0]
        for i in range(cols):
            match self.proc.stdout.read(1):
                case b'i':
                    data.append(unpack('i', self.proc.stdout.read(4))[0])
                case b'b':
                    l, = unpack('H', self.proc.stdout.read(2))
                    s = self.proc.stdout.read(l).decode('utf8', 'backslashreplace')
                    data.append(s)
        return tuple(data)
