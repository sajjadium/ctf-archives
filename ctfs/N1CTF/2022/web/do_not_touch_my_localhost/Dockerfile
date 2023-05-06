FROM archlinux:base-20221030.0.98412

# If you are not in China, please delete the next line to diable the pacman mirror
RUN echo 'Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch' > /etc/pacman.d/mirrorlist 
RUN pacman -Syu --noconfirm && pacman -S --noconfirm sed chromium caddy

COPY ./Caddyfile /caddy/Caddyfile
COPY ./start.sh /start.sh
COPY ./app /app

RUN chmod +x /start.sh && \
    chmod +x /app/main && \
    useradd -m app

CMD /start.sh
