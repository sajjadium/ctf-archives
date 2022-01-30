FROM mcr.microsoft.com/mssql/server:2017-latest
COPY ./install.sql /install.sql
COPY ./entrypoint.sh /entrypoint.sh
CMD exec /bin/bash /entrypoint.sh