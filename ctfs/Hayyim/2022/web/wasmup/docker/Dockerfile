FROM archlinux:latest

RUN yes | pacman -Sy emscripten nodejs

RUN useradd -m ctf

WORKDIR /home/ctf

COPY ynetd app.c ./

RUN /usr/lib/emscripten/emcc -o app.js -s NODERAWFS -s EXIT_RUNTIME=1 app.c

USER ctf

CMD ./ynetd -p 2000 'node app.js'
