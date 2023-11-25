# Copyright 2022-2023 USTC-Hackergame
# Copyright 2021 PKU-GeekGame
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from selenium import webdriver
import selenium
import time
import os
import subprocess
import urllib.parse
import random
import re
import atexit

# Stage 1

file_name=input("File name: ").strip()
assert re.match("[a-z]+\.[a-z]+",file_name) and len(file_name)<10
print("Input your file:")

code = ""
while True:
    line = input()
    if line == "EOF":
        break
    code += line + "\n"
    if len(code) > 1024 * 5:
        print("The file can not be larger than 5KB")
        exit(1)

try:
    os.mkdir("/dev/shm/xss-data")
except Exception as e:
    pass

user_id=os.urandom(8).hex()
try:
    os.mkdir("/dev/shm/xss-data/"+user_id)
except Exception as e:
    pass

try:
    os.mkdir("/dev/shm/chromium-data")
except Exception as e:
    pass

with open("/dev/shm/xss-data/"+user_id+"/"+file_name, "w") as f:
    f.write(code)

port_id=str(random.randint(30000,50000))

sp = subprocess.Popen(
    ["python3", "-m", "http.server", "-b", "127.0.0.1", port_id], cwd="/dev/shm/xss-data/"+user_id,
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
time.sleep(1)
if sp.poll() is not None:
    print("Failed to start HTTP server, please try again in a moment")
    exit(1)

def cleanup():
    try:
        os.rmdir("/dev/shm/xss-data/"+user_id)
    except Exception as e:
        pass
    try:
        sp.kill()
    except Exception as e:
        pass

atexit.register(cleanup)

# Stage 2
try:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # sandbox not working in docker
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--user-data-dir=/dev/shm/user-data/"+user_id)
    os.environ["TMPDIR"] = "/dev/shm/chromium-data/"
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    with webdriver.Chrome(options=options) as driver:
        ua = driver.execute_script("return navigator.userAgent")
        print(" I am using", ua)

        driver.set_page_load_timeout(15)

        print("- Now browsing your website...")
        driver.get("http://localhost:"+port_id+"/"+file_name)
        time.sleep(4)
        
        print("Bye bye!")
except Exception as e:
    print("ERROR", type(e))
    print("I'll not give you exception message this time.")
