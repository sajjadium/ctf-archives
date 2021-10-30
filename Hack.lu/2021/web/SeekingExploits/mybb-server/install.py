#!/usr/bin/python3
import requests
import sys
import os
import time
import random
import string
import pymysql
from urllib.parse import urlencode

hostname = os.environ["HOSTNAME"]
flag = os.environ["FLAG"]

headers = {
    'Host': hostname
}


# poll installer script
while True:
    time.sleep(1)
    try:
        response = requests.get("http://localhost/install/index.php")
        if response.status_code == 200:
            break
    except:
        print("got exception")
        continue

install_url = "http://localhost/install/index.php"
sess = requests.Session()

# walk through the installation steps
sess.post(install_url, headers=headers, data={'action': 'license'})
sess.post(install_url, headers=headers, data={'action': 'requirements_check'})
sess.post(install_url, headers=headers, data={'action': 'database_info'})

# install the database
database_body = "action=create_tables&dbengine=mysqli&config[mysqli][dbhost]=database&config[mysqli][dbuser]=root&config[mysqli][dbpass]=supersecretmysqlpasswordnotahint&config[mysqli][dbuser]=root&config[mysqli][dbname]=mybb&config[mysqli][encoding]=utf8&config[mysqli][tableprefix]=mybb_"
res = sess.post(install_url, headers={'Content-Type': 'application/x-www-form-urlencoded', 'Host': hostname}, data=database_body)

# insert default data
sess.post(install_url, headers=headers, data={'action': 'populate_tables'})
sess.post(install_url, headers=headers, data={'action': 'templates'})
sess.post(install_url, headers=headers, data={'action': 'configuration'})

res = sess.post(install_url, headers=headers, data={
    'action': 'adminuser',
    'bbname': 'SeekingExploits',
    'bburl': 'http://' + hostname,
    'websiteurl': 'http://' + hostname,
    'websitename': 'SeekingExploits',
    'cookiedomain': '',
    'contactemail': 'admin@' + hostname,
    'pin': ''

})

# set up adminuser account
password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
admin_config = {
    'action': 'final',
    'adminuser': 'admin',
    'adminpass': password,
    'adminpass2': password,
    'adminemail': 'admin@' + hostname
}

res = sess.post(install_url, headers=headers, data=admin_config)

# give the database some time to boot
time.sleep(30)

# enable some non-default settings
db = pymysql.connect("database","root","supersecretmysqlpasswordnotahint","mybb")
cursor = db.cursor()

# Enable instant activation registration on the server
cursor.execute("UPDATE mybb_settings SET value='instant' WHERE name='regtype';")

# put the flag into the private notes of the admin
cursor.execute("UPDATE mybb_users SET usernotes='{}' WHERE username='admin';".format(flag))

# enable the emarket plugin
cursor.execute("UPDATE mybb_datacache SET cache='{}' WHERE title='plugins';".format('a:1:{s:6:"active";a:1:{s:7:"emarket";s:7:"emarket";}}'))

cursor.close()


# finally, delete the installation dir and the .htaccess file and expose the instance
os.system("rm -rf install/")
os.system("rm .htaccess")

# loop to keep the docker image alive
while True:
    time.sleep(20)