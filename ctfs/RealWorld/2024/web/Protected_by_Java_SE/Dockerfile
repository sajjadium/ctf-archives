FROM ubuntu:22.04

RUN apt update
RUN apt install -y wget git
RUN mkdir /codeql
RUN wget https://github.com/github/codeql-action/releases/download/codeql-bundle-v2.15.5/codeql-bundle-linux64.tar.gz
RUN tar -xzf codeql-bundle-linux64.tar.gz -C /codeql
RUN rm codeql-bundle-linux64.tar.gz
RUN useradd -m ctf
RUN mkdir /app
RUN chown ctf:ctf /app
COPY codeql_agent /app/codeql_agent
RUN chmod 555 /app/codeql_agent
COPY flag /flag
RUN chmod 444 /flag
USER ctf
WORKDIR /app
CMD [ "./codeql_agent" ]
