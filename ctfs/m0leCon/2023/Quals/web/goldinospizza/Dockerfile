FROM debian:latest AS goldinospizza

# USERS
RUN addgroup --system appgroup --gid 1000 && adduser --ingroup appgroup --system appuser --uid 1000

WORKDIR /tmp
RUN apt-get update

# flask
RUN mkdir -p "/root/flask" && chmod -R "o=rX" "/root"
WORKDIR /root/flask
# # install dependencies
RUN apt-get install --no-install-recommends --upgrade -y python3 python3-pip
# init flask dependencies
COPY "flask/requirements.txt" "requirements.txt"
RUN chmod -R "o=rX" "/root"
USER appuser
RUN python3 -m pip install --no-cache-dir --upgrade -r "requirements.txt"
USER root
# clean some dependencies after build
RUN apt-get purge -y python3-pip
# init flask
COPY "flask/api.py" "flask/auth.py" "flask/server.py" "flask/website.py" ./
COPY "flask/models" "./models"
COPY "flask/static" "./static"
COPY "flask/templates" "./templates"
RUN chmod -R "o=rX" "/root"
# init https
# COPY "flask/key.pem" "/run/secrets/key" ./
# COPY "flask/cert.pem" "/run/secrets/cert" ./
# RUN chmod "444" "/run/secrets/key" "/run/secrets/cert"

# CLEANUP APT CACHE
RUN apt-get clean && rm -r /var/lib/apt/lists/*

# RUN
USER appuser:appgroup
WORKDIR /root/flask
EXPOSE 8000
# ENTRYPOINT [ "/usr/local/bin/gunicorn", "server:app", \
ENTRYPOINT [ "/home/appuser/.local/bin/gunicorn", "server:app", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "1", \
    "--threads", "16" \
]
#     "--keyfile", "/run/secrets/key", \
#     "--certfile", "/run/secrets/cert" \
# ]
