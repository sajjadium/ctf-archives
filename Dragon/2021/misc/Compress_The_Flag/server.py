#!/usr/bin/env python3
import threading
import socket
import random
import codecs
import lzma as lz


with open("flag.txt", "rb") as f:
  FLAG = f.read().strip()

def none(v):
  return len(v)

def zlib(v):
  return len(codecs.encode(v, "zlib"))

def bzip2(v):
  return len(codecs.encode(v, "bz2"))

def lzma(v):
  return len(lz.compress(v))

COMPRESSION_FUNCS = [
  none,
  zlib,
  bzip2,
  lzma
]

def handle_connection(s, addr):
  s.sendall(
      ("Please send: seed:string\\n\n"
       "I'll then show you the compression benchmark results!\n"
       "Note: Flag has format DrgnS{[A-Z]+}\n").encode())

  data = b''
  while True:
    idx = data.find(b'\n')
    if idx == -1:
      if len(data) > 128:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return

      d = s.recv(1024)
      if not d:
        s.close()
        return
      data += d
      continue

    line = data[:idx]
    data = data[idx+1:]

    seed, string = line.split(b':', 1)

    flag = bytearray(FLAG)
    random.seed(int(seed))
    random.shuffle(flag)
    test_string = string + bytes(flag)

    response = []
    for cfunc in COMPRESSION_FUNCS:
      res = cfunc(test_string)
      response.append(f"{cfunc.__name__:>8} {res:>4}")

    response.append('')
    response.append('')
    s.sendall('\n'.join(response).encode())

  s.shutdown(socket.SHUT_RDWR)
  s.close()


def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 1337))
    s.listen(256)

    while True:
      conn, addr = s.accept()
      print(f"Connection from: {addr}")

      th = threading.Thread(
          target=handle_connection,
          args=(conn, addr),
          daemon=True
      )
      th.start()

if __name__ == "__main__":
  main()

