FROM python:3.10-alpine@sha256:3bfac1caa31cc6c0e796b65ba936f320d1e549d80f5ac02c2e4f83a0f04af3aa


ENV USER accountant

RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN apk add --no-cache curl

# Add files
RUN adduser -D -g "" $USER \
 && chown -R root:root /home/$USER

COPY --chown=root:$USER job.py requirements.txt /home/$USER/
COPY --chown=root:root flag.txt /flag.txt

RUN chmod 444 /flag.txt
RUN mv /flag.txt /$(cat /proc/sys/kernel/random/uuid | sed 's/[-]//g' | head -c 20; echo;)

# chown & chmod files
WORKDIR /home/$USER
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 555 job.py 



CMD while :; do sleep 30; ./job.py; done
USER $USER
