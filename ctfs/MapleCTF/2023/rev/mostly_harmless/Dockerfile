FROM archlinux:latest
RUN pacman -Syu --noconfirm socat mypy
COPY ./src /app
RUN sed -i "s/sys\.setrecursionlimit(2\*\*14)/sys\.setrecursionlimit(2\*\*20)/g" /usr/lib/python3.11/site-packages/mypy/main.py
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:\"python /app/app.py\""]
