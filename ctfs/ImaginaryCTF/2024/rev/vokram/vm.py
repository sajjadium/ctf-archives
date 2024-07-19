#!/usr/bin/env python3
def vokram(text, program):
    while True:
        for pat, repl, stop in program:
            if pat in text:
                text = text.replace(pat, repl, 1)
                if stop:
                    return text
                break
        else:
            return text


def parse(source):
    program = []
    for line in source.strip().splitlines():
        pat, repl = line.split(":", 1)
        stop = False
        if len(repl) > 0 and repl[0] == ":":
            repl = repl[1:]
            stop = True
        if ":" in repl:
            raise ValueError("invalid rule: %r" % line)
        program.append((pat, repl, stop))
    return program


if __name__ == "__main__":
    import sys

    source_file = sys.argv[1]
    input_str = sys.argv[2]
    with open(source_file) as f:
        program = parse(f.read())
    print(vokram(input_str, program))
