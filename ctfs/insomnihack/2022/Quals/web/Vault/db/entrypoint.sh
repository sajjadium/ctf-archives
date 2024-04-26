#!/bin/bash
#start SQL Server
sh -c " 
echo 'Sleeping 20 seconds before running setup script'
sleep 20s

echo 'Starting setup script'

#run the setup script to create the DB and the schema in the DB
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -i /install.sql
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -Q \"use Vault; EXEC dbo.CreateUser @login='admin',@password='$ADMIN_PWD';\"
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -Q \"use Vault; grant select on dbo.Stats to admin;\"
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -Q \"use Vault; EXEC dbo.CreateUser @login='secret',@password='$SECRET_PWD';\"
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -Q \"use Vault; INSERT INTO dbo.Vault (username,secret_name,secret_value) VALUES ('secret','FLAG','$FLAG');\"

echo 'Finished setup script'
exit
" & 
exec /opt/mssql/bin/sqlservr --accept-eula