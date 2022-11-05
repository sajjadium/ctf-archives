<title to be determined>
=====

For this challenge, you are given a shell as an unprivileged user. You can talk with another 'server' process through unix message queues (msgget, msgsnd, msgrcv).

The only process that can read the flag runs as the 'flag' user, but it also communicates with this 'server' process.

You have to exploit the server and then exploit the flag client to get the flag.

The bugs are kindof interesting.
