docker build . -t linectf_babysandbox
docker run -it -d -p 8000:8000 --name linectf_babysandbox linectf_babysandbox