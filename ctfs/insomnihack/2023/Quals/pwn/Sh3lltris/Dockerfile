FROM multiarch/debian-debootstrap:amd64-bullseye-slim
COPY ./shellcode .
COPY ./entrypoint.sh .
COPY flag .
RUN chmod +x ./shellcode && chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
