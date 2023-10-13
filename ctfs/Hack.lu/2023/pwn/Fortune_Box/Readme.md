Wanna test your fortune? Try this small program to predict your future. I grabbed it from our old archive server so it might be a bit dated.
Don't be discouraged from a bad prediction. Future telling is just hocus pocus, or is it?


# Fortune Box
Build the debug container with `docker build -t fortune-box-debug .`.
Start the container with `docker run --rm -ti -p 1337:1337 -v "$PWD":/chall fortune-box-debug`
The process will then listen on port 1337 and spawn the challenge once a connection is started.

A log file `kmsg.log` is create which contains the kernel log output for each run.
It contains information about crashed processes.

The terminal with the docker command will print a pty number, e.g., `/dev/pts/12` where a root shell is spawned.
Exec into the container and connect to the shell with a serial console, e.g., `pyserial-miniterm --raw --eol CR /dev/pts/12`.
The challenge is halted if the fortune-box process crashes, this can be suppressed by creating the file `/debug`, e.g., run `touch /debug` in the vm.

The flag resides in `/flag`.
The message `Unable to load ROM!` is normal and can be ignored.

Now find out what the future brings to you.
