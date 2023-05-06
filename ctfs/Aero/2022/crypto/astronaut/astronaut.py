#!/usr/bin/env python3

import os
import random
from typing import List, Generator


def flight(galaxy: List[int], black_holes: List[int]) -> Generator[int, None, None]:
    while True:
        yield (
            black_holes := black_holes[1:] + [
                sum(x * y for x, y in zip(galaxy, black_holes))
            ]
        )[0]


def main():
    rnd = random.SystemRandom(1337)
    limit = 1000

    galaxy = [rnd.randrange(0, limit) for _ in range(16)]
    black_holes = [rnd.randrange(0, limit) for _ in range(16)]

    emotions = os.getenv('FLAG').strip()
    emptiness = '\0' * 64

    message = (emotions + emptiness).encode()
    astronaut = flight(galaxy, black_holes)

    for memory in message:
        print(memory ^ next(astronaut) % limit, end = ' ')


if __name__ == '__main__':
    main()
