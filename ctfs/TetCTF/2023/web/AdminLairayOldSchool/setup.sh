#!/bin/bash

docker-compose up -d --build

sleep 120

docker ps

# SETUP BASIC CONFIG FOR LIFERAY
docker exec -it admin-portal sh -c 'curl -i -s -k -X "POST" -H "Host: localhost:8080" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0" -H "Content-Type: application/x-www-form-urlencoded" -H "Content-Length: 436" -H "Connection: close" --data-binary "formDate=1672372076699&cmd=update&companyName=Liferay&companyLocale=en_US&adminFirstName=Test&adminLastName=Test&adminEmailAddress=test%40liferay.com&defaultDatabase=true&databaseType=db2&properties--jdbc.default.url--=jdbc%3Ahsqldb%3A%2Fopt%2Fliferay-portal-6.1.2-ce-ga3%2Fdata%2Fhsql%2Flportal&properties--jdbc.default.driverClassName--=org.hsqldb.jdbcDriver&properties--jdbc.default.username--=sa&properties--jdbc.default.password--=" "http://localhost:8080/c/portal/setup_wizard" -L'

sleep 120

# all container up now
# additional settings
./unexpose_docker_port.sh admin-portal 8000

./unexpose_docker_port.sh admin-portal 8009

./unexpose_docker_port.sh admin-portal 8080

./unexpose_docker_port.sh admin-portal 11311

