# docker build -t tex_based_adventure . && docker run --rm -ti tex_based_adventure

# You don't really need to use this, but if your TeX version is old and things
# don't work as expected, this should have the version that I used.
# There's no magic here.

FROM archlinux:latest

RUN pacman -Syu --noconfirm texlive-{bin,most} && \
    rm -rf /var/cache/{pacman,pkgfile}

COPY adventure.tex /
RUN chmod +x /adventure.tex

CMD /adventure.tex
