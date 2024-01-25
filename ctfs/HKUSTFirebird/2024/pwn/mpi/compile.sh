#! /bin/bash
if [ ! -e "mpi" ]; then
	/usr/bin/mpicc ./MPI.c -o mpi
fi
