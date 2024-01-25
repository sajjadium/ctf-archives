Naive distributed message encoding machine.

Note: The task is based on MPI (Message Passing Interface) library, so for testing locally you need to setup environment at first (apt should be enough).

Six files are provided:

    mpi - the MPI task binary deployed on the task server
    flag.txt - fake flag
    MPI.c - source file of the task
    compile.sh - script for compiel the binary, would be useful if you want to compile on you local environment
    exec.sh - MPI wrapper script for executing the binary
    env - the docker environment hosting the task

Note: It's recommended to solve the task with the same environment as the remote server, in case any envoronmental issue causing the exp works locally but not on remote server
