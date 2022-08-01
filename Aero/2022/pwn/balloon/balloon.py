#!/usr/bin/env python3

import os


VERY_NICE = 1337


def execute(payload: str) -> object:
    try:
        return eval(payload)
    except Exception as e:
        return f'[-] {e}'


def main() -> None:
    os.nice(VERY_NICE)

    os.write(1, b'[*] Please, input a payload:\n> ')
    payload = os.read(0, 512).decode()

    os.close(0)

    result = execute(payload)
    print(result)

    os._exit(0)


if __name__ == '__main__':
    main()
