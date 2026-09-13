php-sandbox-escape.md
We built a tiny PHP "scripting" service. `disable_functions` blocks every dangerous builtin we could think of, `open_basedir` locks you into `/home/ctf/scripts` and `/tmp`, and there is no shell to be found. You still have arbitrary PHP evaluation via `POST /index.php` with a `cmd` parameter. The real flag is only readable by root through the setuid `/readflag` helper. Escape the sandbox, get native code execution, and read the flag.

@Rodney98
