import os
import random
import string
import sys
import tempfile
import hashlib
import subprocess
import shutil

BASE = os.path.join(tempfile.gettempdir(), 'sandbox')

sys.stdout.write('''\x1b[31;1m
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣄⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⡶⢿⣟⡛⣿⢉⣿⠛⢿⣯⡈⠙⣿⣦⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⡾⠻⣧⣬⣿⣿⣿⣿⣿⡟⠉⣠⣾⣿⠿⠿⠿⢿⣿⣦⠀⠀⠀
⠀⠀⠀⠀⣠⣾⡋⣻⣾⣿⣿⣿⠿⠟⠛⠛⠛⠀⢻⣿⡇⢀⣴⡶⡄⠈⠛⠀⠀⠀
⠀⠀⠀⣸⣿⣉⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠈⢿⣇⠈⢿⣤⡿⣦⠀⠀⠀⠀
⠀⠀⢰⣿⣉⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⠀⢻⣦⠾⣆⠀⠀⠀
⠀⠀⣾⣏⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡶⢾⡀⠀⠀
⠀⠀⣿⠉⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⣼⡇⠀⠀
⠀⠀⣿⡛⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣧⣼⡇⠀⠀
⠀⠀⠸⡿⢻⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣥⣽⠁⠀⠀
⠀⠀⠀⢻⡟⢙⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣧⣸⡏⠀⠀⠀
⠀⠀⠀⠀⠻⣿⡋⣻⣿⣿⣿⣦⣤⣀⣀⣀⣀⣀⣠⣴⣿⣿⢿⣥⣼⠟⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠻⣯⣤⣿⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣷⣴⡿⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠾⣧⣼⣟⣉⣿⣉⣻⣧⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
\x1b[0m''')


def prompt_code():
    sys.stdout.write('Welcome to the ouroboros challenge, give me your code: (empty line to end)\n')
    sys.stdout.flush()
    code = ""
    w = input()
    while w:
        code += w + '\n'
        w = input()
    return code


def run_code(code, stdin):
    if not code.strip():
        sys.stderr.write('Your code was so short it couldn\'t find its own tail.\n')
        sys.stdout.flush()
        return
    if len(code) > 99999:
        sys.stderr.write('Your code was so long it couldn\'t find its own tail.\n')
        sys.stdout.flush()
        return
    h = hashlib.sha256(code.encode()).hexdigest()
    jobdir = os.path.join(BASE, h)
    os.makedirs(jobdir, exist_ok=True)
    sandbox_root = os.path.join(jobdir, 'root')
    os.makedirs(sandbox_root, exist_ok=True)

    src_path = os.path.join(jobdir, 'main.c')
    with open(src_path, 'w') as f:
        f.write(code)

    bin_path = os.path.join(sandbox_root, 'main')
    proc = subprocess.run([
        'gcc', '-O0', '-std=c99', '-fno-common', '-pipe', '-static', '-nostdlib', '-o', bin_path,
        src_path,
    ], capture_output=True)
    os.remove(src_path)

    if proc.returncode != 0:
        sys.stdout.write('Your code was so bad it couldn\'t find its own tail.\n')
        sys.stdout.flush()
        print(proc.stderr.decode(), file=sys.stderr)
        shutil.rmtree(jobdir)
        return
    nsjail_cmd = [
        "nsjail",
        "--mode", "o",
        "--user", "99999",
        "--group", "99999",
        "--disable_proc",
        "--disable_clone_newnet",
        "--disable_clone_newipc",
        "--disable_clone_newuts",
        "--disable_clone_newpid",
        "--rlimit_as", "64",
        "--rlimit_cpu", "1",
        "--rlimit_fsize", "1",
        "--rlimit_nofile", "1",
        "--rlimit_nproc", "1",
        "--chroot", sandbox_root,
        "--bindmount_ro", f"{sandbox_root}:/",
        "--seccomp_string", "ALLOW { read, write, close, execve, exit_group } DEFAULT KILL_PROCESS",
        "--",
        "/main",
    ]
    proc = subprocess.run(
        nsjail_cmd,
        input=stdin.encode(),
        capture_output=True,
        timeout=1,
    )
    out = proc.stdout.decode().strip()
    shutil.rmtree(jobdir)
    if proc.returncode != 0:
        sys.stdout.write('Your code was so bad it died.\n')
        sys.stdout.flush()
        return
    return out


def _reverse():
    s = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
    return s, s[::-1]


def _sum():
    nums = [random.randint(0, 20) for _ in range(random.randint(3, 7))]
    return f'{len(nums)} {" ".join(map(str, nums))}', sum(nums)


def _is_prime():
    n = random.randint(2, 100)
    prime = n > 1 and all(n % i for i in range(2, int(n**0.5) + 1))
    return n, prime


def _fibonacci():
    n = random.randint(1, 15)
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return n, b


def _caesar():
    shift = random.randint(1, 25)
    text = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 12)))
    encoded = ''.join(
        chr((ord(c) - 97 + shift) % 26 + 97) if 'a' <= c <= 'z' else c
        for c in text
    )
    return f'{shift} {text}', encoded


def task():
    fn = random.choice([_reverse, _sum, _is_prime, _fibonacci, _caesar])
    return fn.__name__[1:], *fn()


def main():
    original = code = prompt_code()
    tasks = [task() for _ in range(69)]
    code = run_code(code, tasks[0][0])
    if code is None:
        return
    for i, (_, input_data, expected_output) in enumerate(tasks):
        sys.stdout.write(f'task {i+1}/{len(tasks)}\n')
        sys.stdout.flush()
        out = run_code(code, str(input_data) + '\n'+(tasks[i+1][0] if i + 1 < len(tasks) else ''))
        if out is None:
            return
        ans = out[:out.find('\n')] if '\n' in out else out
        code = out[out.find('\n')+1:] if '\n' in out else ''
        if ans != str(expected_output):
            sys.stdout.write('Your code was so bad it couldn\'t find its own tail.\n')
            sys.stdout.flush()
            return
    if original.strip() != code.strip():
        sys.stdout.write('Your code was so bad it couldn\'t find its own tail.\n')
        print(code)
        print("\n\n")
        print(original)
        return
    else:
        sys.stdout.write('Your code was a true ouroboros!\n')
        sys.stdout.write(os.environ.get('FLAG', 'flag{this_is_a_fake_flag}') + '\n')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
