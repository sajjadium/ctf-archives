FROM ocaml/opam2:4.10

USER root

COPY ./tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--", "opam", "config", "exec", "--"]

USER opam

RUN opam update && opam install -y dune

WORKDIR /home/opam/sos

USER root

COPY --chown=opam:opam ./src/ ./
COPY --chown=opam:opam ./flag /flag

RUN chown opam:opam /home/opam/sos
RUN rm /etc/sudoers.d/opam && chmod 0755 ./main && chmod 0644 /flag

USER opam

CMD [ "./main" ]
