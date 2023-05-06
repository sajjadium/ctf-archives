#!/usr/bin/env python3
import secrets
import os
import time

os.chdir("/app")
requestID = secrets.token_hex(16)
os.mkdir(f"./request/{requestID}")

pidPath = f"{os.getcwd()}/request/{requestID}/fpm.pid"
sockPath = f"{os.getcwd()}/request/{requestID}/fpm.sock"
confPath = f"{os.getcwd()}/request/{requestID}/php-fpm.conf"

phpfpmConf = f"""
[global]
pid = {pidPath}
error_log = syslog
[www]
listen = {sockPath}
pm = static
pm.max_children = 1
pm.process_idle_timeout = 3s;
""".strip()

confFile = open(confPath,"w")
confFile.write(phpfpmConf)
confFile.close()

os.system(f"timeout 2 php-fpm -F -y {confPath} -c ./php.ini 2>/dev/null 1>/dev/null &")
while(os.path.exists(sockPath) == False):
	time.sleep(0.001)
os.system(f"timeout 2 ./app.py {sockPath}")
os.system(f"`sleep 3;rm -r ./request/{requestID}` 2>/dev/null >/dev/null &")
