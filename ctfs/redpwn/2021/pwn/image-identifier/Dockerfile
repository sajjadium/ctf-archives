FROM redpwn/jail:v0.0.2

# ubuntu:bionic
COPY --from=ubuntu@sha256:ce1e17c0e0aa9db95cf19fb6ba297eb2a52b9ba71768f32a74ab39213c416600 / /srv

COPY bin/chal /srv/app/run
COPY bin/flag.txt /srv/app/flag.txt
