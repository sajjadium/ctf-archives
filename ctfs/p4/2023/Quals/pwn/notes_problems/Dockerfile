FROM patryk4815/nsjail:23.04

WORKDIR /home/notes
COPY notes entrypoint.sh ./
COPY flag.txt ./

EXPOSE 4000/tcp
CMD /home/notes/entrypoint.sh
