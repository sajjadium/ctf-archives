service apache2 start
echo "127.0.0.1 api.prodnotes.bb">>/etc/hosts
python3 app.py
