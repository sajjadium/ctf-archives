#!/usr/local/bin/python3

import time
from tempfile import TemporaryDirectory

with TemporaryDirectory() as workdir:
    __import__('os').chdir(workdir)
    __import__('os').mkdir('runtime')

    print("Enter a reverse quine. It must print its source code backwards (including any trailing newlines).")
    print("It must be non-empty and contain 0 quotation marks or dunders. All ascii btw. oh and no builtins.")
    print("To prove you wrote it yourself, it must contain the string 'pyquinejailgolf', and be ==343 chars.")
    print("Well...I'm not sure how you're supposed to write a quine without print statements. u can have em.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~ Type <END> to terminate the program input ~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    prog = []
    while (x := input(">>> ")) != "<END>":
        prog.append(x)
    program = "\n".join(i for i in prog)

    assert x == "<END>", "what did you do this time."
    assert all(ord(i) < 128 for i in program), "i don't speak foreign languages."
    assert all(i not in program for i in ['"', "'", '_']), "who uses strings anyway? it's not like quines require strings."
    assert program != "", "scuse me, just cleaning out the garbage."
    assert "pyquinejailgolf" in program, "are you sure you wrote this program yourself?"
    assert len(program) == 343

    import sys
    stdout = sys.stdout
    with open('runtime/trash.txt', 'w+') as sys.stdout:
        goal = time.time_ns() + 5000000000
        try:
            with open('runtime/external_run.py', 'w+') as f:
                f.write(f"""
with open('runtime/output.txt', 'w+') as __import__('sys').stdout:
    {program = }
    safe_builtins = {{}}
    for i in dir(__builtins__):
        if i[0] not in __import__('string').ascii_lowercase:
            safe_builtins[i] = eval(i)
    safe_builtins['print'] = print
    new_builtins = {{'__builtins__':safe_builtins}}
    try:exec(program, new_builtins, new_builtins)
    except:pass""")
            __import__('os').system('timeout 2.5 /usr/local/bin/python3 runtime/external_run.py')
        except:
            pass

    time.sleep(max(0, (goal - time.time_ns())/1e9))
    sys.stdout = stdout
    with open('runtime/output.txt') as f:
        if (c := f.read()[::-1]) == program:
            print("good jorb")
        else:
            exit("bad")

    with open('/app/flag.txt') as f:
        print(f.read())
