export FLAG="X-MAS{SECRET}"
echo "Starting nginx..."
nginx
export ADMIN_COOKIE=$(python3 -c 'import os; print(os.urandom(32).hex(), end="")')
echo "Admin cookie: $ADMIN_COOKIE";
echo "Starting chall website..."
cd /chall
#gunicorn3 --workers=1 --worker-connections=1024 --worker-class gevent --bind 0.0.0.0:2000 main:app &
su ctf --command "gunicorn3 --workers=1 --threads=4 --worker-class gthread --bind localhost:2000 main:app" &
echo "Starting bot..."
cd /bot
su ctf --command "export DBUS_SESSION_BUS_ADDRESS=/dev/null; while true; do python3 bot.py; done" &
echo "Initialization sequence completed."
while true; do sleep 1000; done
