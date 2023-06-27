#!/usr/bin/env python3
import sys
import os
import secrets
import subprocess

LIMIT: int = 1024

def prep_ini(filepath: str) -> None:
    runner_path = f'{filepath}.runner'
    with open('./conf.ini', 'r') as f:
        ini_template = f.read()
        ini_template = ini_template.replace('<RUNNER_PATH>', f'{runner_path}')

    with open(f'{filepath}.ini', 'w') as f:
        f.write(ini_template)

    with open(runner_path, 'w') as f:
        f.write(f'<?php opcache_compile_file("{filepath}"); ?>')


def run_php(filepath: str) -> None:
    prep_ini(filepath)
    argv = ['/usr/local/bin/php', '-c', f'{filepath}.ini', '-f', filepath]
    subprocess.call(argv)
    os.remove(filepath)
    os.remove(f'{filepath}.ini')
    os.remove(f'{filepath}.runner')

def dump_contents(filepath: str, data: str) -> None:
    with open(filepath, 'w') as f:
        f.write(data)

if __name__ == '__main__':
    sys.stdout.write('Send your script between "<?php" and "?>" tags for PHP execution(i.e: `<?php echo "Hello World\\n"; ?>`) \n')
    sys.stdout.flush()
    data = sys.stdin.readline(LIMIT)
    if not data:
        exit(0)

    filepath = f'/tmp/{secrets.token_hex(16)}.php'
    dump_contents(filepath, data)
    run_php(filepath)
