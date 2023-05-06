memcached -d -m 50 -p 11200 -u root 
python3 ./app.py
tail -f /dev/null