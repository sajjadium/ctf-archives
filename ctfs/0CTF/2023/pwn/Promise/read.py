import sys
import os

def main():
    if not os.path.exists(sys.argv[1]):
        return
    print('Please input script:')
    script = sys.stdin.read(30000)
    end = script.find('EOF')
    if end != -1:
        script = script[:end]
    with open(sys.argv[1], 'w') as f:
        f.write(script)

if __name__ == '__main__':
    main()
