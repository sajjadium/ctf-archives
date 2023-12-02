FROM --platform=linux/amd64 ubuntu:20.04 as deps

# use the jail base image
FROM --platform=linux/amd64 pwn.red/jail
# copy the root files from any Docker image
COPY --from=deps / /srv
# setup the binary to run
RUN mkdir /srv/app
COPY flag.txt /srv/app/flag.txt
COPY heapnotes /srv/app/run
