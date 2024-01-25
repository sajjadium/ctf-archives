It's time for lua pwn.

The task is based on a patched version of the lua compiler, you need to analyze the patched function and try to exploit and get the flag.

Three files are provided:

    lua - the patched lua binary file
    task.diff - the patch based on https://github.com/lua/lua with commit id 7923dbbf72da303ca1cca17efd24725668992f15
    env - the docker environment hosting the task

Note: It's recommended to solve the task with the same environment as the remote server, in case any envoronmental issue causing the exp works locally but not on remote server
