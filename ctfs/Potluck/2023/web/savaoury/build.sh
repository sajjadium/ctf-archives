docker build --build-arg 'FLAG=potluck{placeholder_flag}' --tag savaoury_chall .
docker run -p 80:8631 -p 443:8632 --name savaoury -it savaoury_chall