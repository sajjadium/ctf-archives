import sys
import io
import subprocess

def main():
  reader = io.BufferedReader(sys.stdin.buffer, buffer_size=1)

  print('File size:', flush=True)
  input_size = int(reader.readline())
  if input_size <= 0 or input_size > 65536:
    print('Invalid file size.', flush=True)
    return

  print('File data:', flush=True)
  input_data = reader.read(input_size)
  with open('/tmp/data', 'wb') as f:
    f.write(input_data)

  process = subprocess.Popen(
      ['./challenge', '/tmp/data'],
      stdin=subprocess.DEVNULL,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)
  outs, errs = process.communicate()
  sys.stdout.buffer.write(outs)
  sys.stdout.buffer.write(errs)
  sys.stdout.flush()


if __name__ == '__main__':
  main()
